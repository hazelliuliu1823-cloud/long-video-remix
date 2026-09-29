#!/usr/bin/env python3
"""Validate core references and timing only; never certifies editorial truth."""
import json
import math
import sys
from pathlib import Path


def validate(root):
    errors, warnings, checked, skipped = [], [], [], []

    def require(condition, message):
        if not condition:
            errors.append(message)
        return condition

    def integer(value):
        return type(value) is int

    def positive(value):
        return integer(value) and value > 0

    def load(name, default):
        path = root / name
        if not path.exists():
            skipped.append(name)
            return default
        checked.append(name)
        try:
            if name.endswith('.jsonl'):
                return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
            result = json.loads(path.read_text(encoding='utf-8'))
            if not isinstance(result, type(default)):
                raise ValueError('unexpected top-level type')
            return result
        except (ValueError, OSError) as exc:
            errors.append(f'{name}: {exc}')
            return default

    def index(rows, key):
        result = {}
        for row in rows:
            if not require(isinstance(row, dict), f'{key}: row must be object'):
                continue
            value = row.get(key)
            if not require(isinstance(value, str) and bool(value), f'missing {key}'):
                continue
            require(value not in result, f'duplicate {key}: {value}')
            result[value] = row
        return result

    sources = index(load('sources.json', []), 'source_id')
    if not sources:
        warnings.append('No source records; this is not an executable media project.')
    for sid, source in sources.items():
        require(positive(source.get('duration_ms')), f'{sid}: duration_ms must be positive integer')
        if not source.get('version'):
            warnings.append(f'{sid}: source version unknown; do not reuse precise-cut cache')

    def interval(sid, start, end, label):
        if not require(sid in sources, f'{label}: unknown source {sid}'):
            return False
        if not require(integer(start) and integer(end), f'{label}: times must be integer milliseconds'):
            return False
        duration = sources[sid].get('duration_ms')
        return require(positive(duration) and 0 <= start < end <= duration, f'{label}: invalid or out-of-source range')

    frames = index(load('frames.jsonl', []), 'frame_id')
    for fid, row in frames.items():
        t = row.get('timestamp_ms')
        interval(row.get('source_id'), t, t + 1 if integer(t) else None, fid)

    transcript = index(load('transcript.jsonl', []), 'utterance_id')
    for tid, row in transcript.items():
        interval(row.get('source_id'), row.get('start_ms'), row.get('end_ms'), tid)

    reviews = index(load('reviews.jsonl', []), 'review_id')
    for rid, row in reviews.items():
        interval(row.get('source_id'), row.get('start_ms'), row.get('end_ms'), rid)

    def covered_review(refs, sid, start, end, modality):
        ranges = []
        for ref in refs:
            row = reviews.get(ref, {})
            a, b = row.get('start_ms'), row.get('end_ms')
            if row.get('source_id') == sid and modality in row.get('modalities', []) and integer(a) and integer(b):
                ranges.append((a, b))
        cursor = start
        for a, b in sorted(ranges):
            if a > cursor:
                break
            cursor = max(cursor, b)
        return cursor >= end

    units = index(load('units.jsonl', []), 'unit_id')
    for uid, unit in units.items():
        valid = interval(unit.get('source_id'), unit.get('start_ms'), unit.get('end_ms'), uid)
        protected = unit.get('protected_ranges', [])
        if not require(isinstance(protected, list), f'{uid}: protected_ranges must be array'):
            protected = []
        for p in protected:
            if not require(isinstance(p, dict), f'{uid}: protected range must be object'):
                continue
            a, b = p.get('start_ms'), p.get('end_ms')
            if valid:
                require(integer(a) and integer(b) and unit['start_ms'] <= a < b <= unit['end_ms'], f'{uid}: protected range outside unit')
        tids = unit.get('utterance_ids', [])
        if not require(isinstance(tids, list), f'{uid}: utterance_ids must be array'):
            tids = []
        for tid in tids:
            if require(isinstance(tid, str) and tid in transcript, f'{uid}: unknown utterance {tid}'):
                require(transcript[tid].get('source_id') == unit.get('source_id'), f'{uid}: utterance source mismatch')

    timeline = load('timeline.json', {})
    events = timeline.get('events', [])
    if not require(isinstance(events, list), 'timeline.events must be array'):
        events = []
    event_index = index(events, 'event_id')
    ready = timeline.get('status') == 'ready_for_render'
    if ready:
        require(bool(events), 'ready_for_render has no events')
        require(positive(timeline.get('width')) and positive(timeline.get('height')), 'ready_for_render requires output dimensions')
    fps_num, fps_den = timeline.get('fps_num'), timeline.get('fps_den')
    fps_ok = positive(fps_num) and positive(fps_den)
    if events:
        require(fps_ok, 'timeline requires positive integer fps_num/fps_den')
    frame_ms = 1000 * fps_den / fps_num if fps_ok else None
    cursor = 0
    for event in event_index.values():
        eid = event['event_id']
        a, b = event.get('out_in_frame'), event.get('out_out_frame')
        out_ok = integer(a) and integer(b) and 0 <= a < b
        require(out_ok, f'{eid}: invalid output frame range')
        if out_ok:
            require(a == cursor, f'{eid}: primary timeline has gap, overlap, or wrong order')
            cursor = b
        kind = event.get('kind')
        require(kind in ('source', 'card'), f'{eid}: unsupported event kind')
        if kind != 'source':
            continue
        sid = event.get('source_id')
        start, end = event.get('source_in_ms'), event.get('source_out_ms')
        valid = interval(sid, start, end, eid)
        speed = event.get('speed', 1)
        speed_ok = type(speed) in (int, float) and math.isfinite(speed) and speed > 0
        require(speed_ok, f'{eid}: invalid speed')
        if valid and out_ok and fps_ok and speed_ok:
            require(abs((end - start) / speed - (b - a) * frame_ms) <= frame_ms + 0.001, f'{eid}: source/output duration mismatch')
        uid = event.get('unit_id')
        if not require(isinstance(uid, str) and uid in units, f'{eid}: unknown unit {uid}'):
            continue
        unit = units[uid]
        require(unit.get('source_id') == sid, f'{eid}: unit/source mismatch')
        if valid and integer(unit.get('start_ms')) and integer(unit.get('end_ms')):
            require(unit['start_ms'] <= start < end <= unit['end_ms'], f'{eid}: cut outside unit')
            for p in unit.get('protected_ranges', []):
                if isinstance(p, dict) and integer(p.get('start_ms')) and integer(p.get('end_ms')):
                    require(start <= p['start_ms'] < p['end_ms'] <= end, f'{eid}: cut drops protected meaning range')
        if ready:
            require(bool(sources.get(sid, {}).get('version')), f'{eid}: source version must be known')
            verification = unit.get('verification', {})
            require(isinstance(verification, dict), f'{uid}: verification must be object')
            if isinstance(verification, dict):
                require(all(verification.get(k) in ('reviewed', 'not_applicable') for k in ('audio', 'visual', 'context')), f'{uid}: source review incomplete')
                refs = verification.get('review_refs', [])
                if not require(isinstance(refs, list) and bool(refs), f'{uid}: missing review references'):
                    refs = []
                valid_refs = [ref for ref in refs if isinstance(ref, str) and ref in reviews]
                require(len(valid_refs) == len(refs), f'{uid}: unknown review reference')
                if valid:
                    for name, modality in [('audio', 'audio'), ('visual', 'video')]:
                        if verification.get(name) == 'reviewed':
                            require(covered_review(valid_refs, sid, start, end, modality), f'{uid}: {modality} review does not cover selected range')
                for name in ('audio', 'visual', 'context'):
                    if verification.get(name) == 'not_applicable':
                        reasons = verification.get('not_applicable_reasons', {})
                        require(isinstance(reasons, dict) and bool(reasons.get(name)), f'{uid}: missing reason for {name} not_applicable')
            require(bool(unit.get('protected_ranges')) or bool(unit.get('protection_note')), f'{uid}: missing protection decision')

    transitions = load('transitions.json', [])
    pairs = list(zip(list(event_index)[:-1], list(event_index)[1:]))
    seen = []
    relations = {'continuous', 'ellipsis', 'comparison', 'flashback', 'chapter_change'}
    for row in transitions:
        if not require(isinstance(row, dict), 'transition must be object'):
            continue
        pair = (row.get('from_event'), row.get('to_event'))
        require(pair in pairs, f'transition {pair}: not adjacent events')
        require(pair not in seen, f'transition {pair}: duplicate')
        seen.append(pair)
        require(row.get('relation') in relations, f'transition {pair}: invalid relation')
    if events:
        require(set(seen) == set(pairs), 'every adjacent event pair needs a transition record')

    for key in ('audio_tracks', 'text_tracks'):
        tracks = timeline.get(key, [])
        if not require(isinstance(tracks, list), f'{key}: must be array'):
            continue
        for number, row in enumerate(tracks):
            label = f'{key}[{number}]'
            if not require(isinstance(row, dict), f'{label}: must be object'):
                continue
            a, b = row.get('out_in_frame'), row.get('out_out_frame')
            if row.get('anchor_event_id'):
                anchor = event_index.get(row['anchor_event_id'])
                if require(anchor is not None, f'{label}: unknown event anchor'):
                    la, lb = row.get('local_in_frame'), row.get('local_out_frame')
                    if require(integer(la) and integer(lb), f'{label}: local frames must be integers'):
                        a, b = anchor['out_in_frame'] + la, anchor['out_in_frame'] + lb
            require(integer(a) and integer(b) and 0 <= a < b <= cursor, f'{label}: outside output')
            if key == 'audio_tracks' and row.get('source_id'):
                interval(row['source_id'], row.get('source_in_ms'), row.get('source_out_ms'), label)
    if ready and any(e.get('kind') == 'source' for e in event_index.values()):
        require(bool(timeline.get('audio_tracks')), 'ready_for_render requires explicit audio decisions')
    return {'status': 'fail' if errors else 'pass', 'scope': 'core static references and timing only', 'checked': checked, 'skipped': skipped, 'errors': errors, 'warnings': warnings}


if __name__ == '__main__':
    if len(sys.argv) != 2 or not Path(sys.argv[1]).is_dir():
        print('Usage: validate_project.py PROJECT_DIRECTORY', file=sys.stderr)
        sys.exit(2)
    report = validate(Path(sys.argv[1]))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(1 if report['errors'] else 0)
