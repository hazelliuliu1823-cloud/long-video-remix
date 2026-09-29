#!/usr/bin/env python3
"""Compile an assembly plan to output frames. Does not render media."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def read(path, default=None):
    if not path.exists():
        if default is not None:
            return default
        raise ValueError(f'Missing input: {path.name}')
    if path.suffix == '.jsonl':
        return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    return json.loads(path.read_text(encoding='utf-8'))


def integer(value, label, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f'{label} must be integer >= {minimum}')
    return value


def compile_manifest(root):
    timeline = read(root / 'timeline.json')
    if timeline.get('coordinate_space') != 'assembly':
        raise ValueError('Input must explicitly use coordinate_space=assembly; do not compile output twice')
    project = read(root / 'project.json', {})
    source_rows = read(root / 'sources.json', [])
    sources = {s['source_id']: s for s in source_rows}
    if len(sources) != len(source_rows):
        raise ValueError('Duplicate source_id')
    units = {u['unit_id']: u for u in read(root / 'units.jsonl', [])}
    transition_rows = read(root / 'transitions.json', [])
    transitions = {(x['from_event'], x['to_event']): x for x in transition_rows}
    if len(transitions) != len(transition_rows):
        raise ValueError('Duplicate transition')
    n = integer(timeline.get('fps_num'), 'fps_num', 1)
    d = integer(timeline.get('fps_den'), 'fps_den', 1)
    width = integer(timeline.get('width'), 'width', 1)
    height = integer(timeline.get('height'), 'height', 1)
    frame_ms = 1000 * d / n
    original_events = timeline.get('events', [])
    if not original_events:
        raise ValueError('No video events')
    ids = [e['event_id'] for e in original_events]
    if len(set(ids)) != len(ids):
        raise ValueError('Duplicate event_id')
    if set(transitions) != set(zip(ids[:-1], ids[1:])):
        raise ValueError('Exactly one transition is required for every adjacent pair')
    events, joins, warnings = [], [], []
    assembly_end = 0
    lengths = []
    overlaps = []
    for i, original in enumerate(original_events):
        e = dict(original)
        a = integer(e.get('out_in_frame'), 'assembly start')
        b = integer(e.get('out_out_frame'), 'assembly end', 1)
        if a != assembly_end or b <= a:
            raise ValueError('Assembly events must be contiguous, ordered and nonempty')
        length = b - a
        lengths.append(length)
        assembly_end = b
        overlap = 0
        transition = None
        if i:
            transition = transitions[(ids[i - 1], ids[i])]
            effect = transition.get('effect', 'hard_cut')
            overlap = integer(transition.get('overlap_frames', 0), 'overlap_frames')
            if effect not in ('hard_cut', 'xfade') or (effect == 'hard_cut' and overlap) or (effect == 'xfade' and overlap == 0):
                raise ValueError('Use hard_cut with zero overlap or xfade with positive overlap')
            if overlap >= min(lengths[-2], length):
                raise ValueError('Overlap must be shorter than both adjacent events')
            if i > 1 and overlaps[-1] + overlap >= lengths[-2]:
                raise ValueError('Three-event overlap or zero stable middle segment is unsupported')
        overlaps.append(overlap)
        start = events[-1]['out_out_frame'] - overlap if events else 0
        e.update(out_in_frame=start, out_out_frame=start + length,
                 assembly_in_frame=a, assembly_out_frame=b)
        if e.get('kind') == 'source':
            sid = e.get('source_id')
            if sid not in sources or not sources[sid].get('version'):
                raise ValueError(f'{sid}: known source version required')
            source = sources[sid]
            sin = integer(e.get('source_in_ms'), 'source_in_ms')
            sout = integer(e.get('source_out_ms'), 'source_out_ms', 1)
            duration = integer(source.get('duration_ms'), 'source duration', 1)
            speed = e.get('speed', 1)
            if type(speed) not in (float, int) or not 0 < speed < float('inf'):
                raise ValueError('Invalid speed')
            if not sin < sout <= duration or abs((sout - sin) / speed - length * frame_ms) > frame_ms + 0.001:
                raise ValueError(f'{e["event_id"]}: source length and frozen frame count disagree')
            if e.get('unit_id') not in units:
                raise ValueError(f'{e["event_id"]}: missing unit')
            unit = units[e['unit_id']]
            if unit.get('source_id') != sid or not unit['start_ms'] <= sin < sout <= unit['end_ms']:
                raise ValueError(f'{e["event_id"]}: cut outside unit')
            for protected in unit.get('protected_ranges', []):
                if not sin <= protected['start_ms'] < protected['end_ms'] <= sout:
                    raise ValueError(f'{e["event_id"]}: cut drops protected range')
            e['source_version'] = source['version']
        elif e.get('kind') != 'card':
            raise ValueError('Video event must be source or card')
        events.append(e)
        if i:
            joins.append({'join_id': f'J{i:03d}', 'from_event': ids[i - 1], 'to_event': ids[i],
                          'effect': transition.get('effect', 'hard_cut'), 'relation': transition.get('relation'),
                          'start_frame': start, 'end_frame': start + overlap,
                          'overlap_frames': overlap})
    total = events[-1]['out_out_frame']
    event_map = {e['event_id']: e for e in events}
    for i, join in enumerate(joins):
        if not join['overlap_frames']:
            continue
        trans = transitions[(join['from_event'], join['to_event'])]
        affected = []
        for e in (events[i], events[i + 1]):
            if e['kind'] != 'source':
                continue
            for p in units[e['unit_id']].get('protected_ranges', []):
                pa = e['out_in_frame'] + (p['start_ms'] - e['source_in_ms']) / e.get('speed', 1) / frame_ms
                pb = e['out_in_frame'] + (p['end_ms'] - e['source_in_ms']) / e.get('speed', 1) / frame_ms
                if max(pa, join['start_frame']) < min(pb, join['end_frame']):
                    affected.append(e['event_id'])
        if affected and not trans.get('overlap_protection_review'):
            raise ValueError(f'{join["join_id"]}: overlap covers protected meaning in {affected}')
        if affected:
            warnings.append(f'{join["join_id"]}: protected overlap exception needs actual review: {trans["overlap_protection_review"]}')
    compiled_tracks = {}
    for key in ('audio_tracks', 'text_tracks'):
        result = []
        for row in timeline.get(key, []):
            item = dict(row)
            if item.get('anchor_event_id'):
                if item['anchor_event_id'] not in event_map:
                    raise ValueError('Unknown track anchor_event_id')
                e = event_map[item['anchor_event_id']]
                local_a, local_b = item.get('local_in_frame'), item.get('local_out_frame')
                if type(local_a) is not int or type(local_b) is not int or local_b <= local_a:
                    raise ValueError('Track local range must use integer frames')
                # Explicitly permits J/L-cuts beyond one event, within the full output.
                a, b = e['out_in_frame'] + local_a, e['out_in_frame'] + local_b
            elif item.get('coordinate_space') == 'output':
                a, b = item.get('out_in_frame'), item.get('out_out_frame')
                warnings.append(f'{key}: absolute output position must be rechecked after structural edits')
            else:
                raise ValueError(f'{key}: supply an event anchor or explicit output coordinates')
            if type(a) is not int or type(b) is not int or not 0 <= a < b <= total:
                raise ValueError(f'{key}: track falls outside compiled output')
            item.update(out_in_frame=a, out_out_frame=b, coordinate_space='output')
            if key == 'text_tracks':
                timing = [item.get(k, 0) for k in ('fade_in_frames', 'stable_hold_frames', 'fade_out_frames')]
                if any(type(v) is not int or v < 0 for v in timing) or sum(timing) > b - a:
                    raise ValueError('Text fade and hold exceed display range')
            result.append(item)
        compiled_tracks[key] = result
    render_options = project.get('render_options', {})
    tools = project.get('tool_versions', {})
    unit_keys = {}
    for e in events:
        # Deliberately excludes placement and overlay text; excludes neither trims nor length.
        fields = ['kind', 'source_id', 'source_version', 'source_in_ms', 'source_out_ms', 'speed', 'crop', 'scale', 'card_asset', 'background']
        recipe = {k: e.get(k) for k in fields}
        recipe.update(frames=e['out_out_frame'] - e['out_in_frame'], width=width, height=height,
                      fps=[n, d], options=render_options.get('video', {}), tools=tools)
        unit_keys[e['event_id']] = digest(recipe)
    layout = [{k: e[k] for k in ('event_id', 'out_in_frame', 'out_out_frame')} for e in events]
    clean_key = digest([unit_keys, layout, joins, render_options.get('video', {})])
    audio_key = digest([compiled_tracks['audio_tracks'], layout, joins, {k: v.get('version') for k, v in sources.items()}, project.get('audio_policy'), render_options.get('audio', {}), tools])
    final_key = digest([clean_key, audio_key, compiled_tracks['text_tracks'], render_options.get('final', {}), tools])
    if not tools:
        warnings.append('tool_versions empty: keys are planning identifiers; cache reuse is disabled')
    quiet_ranges = project.get('expected_quiet_ranges', [])
    for q in quiet_ranges:
        a, b = q.get('start_frame'), q.get('end_frame')
        if type(a) is not int or type(b) is not int or not 0 <= a < b <= total or not q.get('reason'):
            raise ValueError('Expected quiet range needs valid output bounds and a reason')
    if quiet_ranges:
        warnings.append('Expected quiet ranges use absolute output positions; recheck after structural edits')
    return {'schema_version': '1.1', 'project_id': timeline.get('project_id'), 'coordinate_space': 'output',
            'fps_num': n, 'fps_den': d, 'width': width, 'height': height, 'total_frames': total,
            'duration_seconds': total * d / n, 'events': events, 'joins': joins, **compiled_tracks,
            'audio_required': project.get('audio_required', True),
            'expected_quiet_ranges': quiet_ranges,
            'cache_keys': {'units': unit_keys, 'clean_video': clean_key, 'mix_audio': audio_key, 'final': final_key},
            'cache_reusable': bool(tools), 'warnings': warnings,
            'input_digest': digest([timeline, transition_rows, source_rows, project, list(units.values())])}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_directory', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        manifest = compile_manifest(args.project_directory)
        destination = args.output or args.project_directory / 'render-manifest.json'
        destination.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({'status': 'compiled_not_rendered', 'file': str(destination), 'frames': manifest['total_frames'], 'warnings': manifest['warnings']}, ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({'status': 'error', 'error': str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
