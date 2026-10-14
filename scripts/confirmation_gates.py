"""Check declared sound/visual decisions; never supplies a user's confirmation."""
import hashlib
import json
import math
import shutil
import subprocess
import wave


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def explicit(value):
    return isinstance(value, str) and value.strip().lower() not in {
        '', 'none', 'unknown', 'pending', 'todo', 'tbd', 'not_applicable', 'null'}


def audio_duration(path):
    """Read WAV locally; use an available ffprobe for other audio formats."""
    try:
        with wave.open(str(path), 'rb') as stream:
            return round(stream.getnframes() * 1000 / stream.getframerate())
    except (wave.Error, EOFError):
        if not shutil.which('ffprobe'):
            raise ValueError('music inspection requires ffprobe for non-PCM-WAV assets')
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
            'format=duration:stream=codec_type', '-of', 'json', str(path)],
            capture_output=True, text=True, timeout=20, check=True)
        info = json.loads(result.stdout)
        if not any(s.get('codec_type') == 'audio' for s in info.get('streams', [])):
            raise ValueError('selected music asset has no audio stream')
        seconds = float(info.get('format', {}).get('duration', 'nan'))
        if not math.isfinite(seconds) or seconds <= 0:
            raise ValueError('selected music duration is unavailable')
        return round(seconds * 1000)


def validate_confirmations(root, project, timeline):
    errors, warnings = [], []
    ready = timeline.get('status') == 'ready_for_render'
    events = {e.get('event_id') for e in timeline.get('events', [])}

    def need(condition, message):
        if not condition:
            errors.append(message)
        return condition

    def read(ref, label):
        try:
            result = json.loads((root / ref).read_text(encoding='utf-8'))
            if not isinstance(result, dict):
                raise ValueError('must be an object')
            return result
        except (OSError, ValueError, TypeError) as exc:
            need(False, f'{label}: {exc}')
            return {}

    def identified(row, label):
        for key in ('decision_id', 'confirmed_by', 'confirmation_source', 'confirmed_at'):
            need(explicit(row.get(key)), f'{label} requires {key}')

    def image_size(ref, label):
        try:
            from PIL import Image
            with Image.open(root / ref) as picture:
                picture.verify()
            with Image.open(root / ref) as picture:
                picture.load()
                return picture.size
        except (ImportError, OSError, ValueError, TypeError, SyntaxError) as exc:
            need(False, f'{label}: readable image required (Pillow): {exc}')
            return None

    music_policy = project.get('music_direction_policy')
    if music_policy is not None:
        need(music_policy == 'mode_confirmation_required', 'invalid music_direction_policy')
    music_ref = project.get('music_direction_ref')
    music_gate = explicit(music_ref) or music_policy == 'mode_confirmation_required'
    if music_gate and ready:
        need(explicit(music_ref) and (root / music_ref).is_file(),
             'ready_for_render requires music direction file and music_direction_ref')
    if explicit(music_ref) and (root / music_ref).is_file():
        music = read(music_ref, 'music-direction')
        status = music.get('status')
        modes = ('narrative_led', 'hybrid', 'music_led')
        need(status in ('draft', 'proposed', 'confirmed'), 'invalid music-direction.status')
        if status in ('proposed', 'confirmed'):
            need(music.get('proposed_mode') in modes, 'music-direction.proposed_mode is invalid')
            need(explicit(music.get('recommendation_reason')), 'music-direction requires recommendation_reason')
        for key in ('protected_event_ids', 'music_flexible_event_ids', 'basis_refs'):
            values = music.get(key)
            need(isinstance(values, list) and all(explicit(x) for x in values),
                 f'music-direction.{key} must be an array of explicit IDs/refs')
        if ready:
            need(status == 'confirmed', 'ready_for_render requires confirmed music mode')
        if status == 'confirmed':
            identified(music, 'confirmed music mode')
            need(music.get('confirmed_mode') in modes, 'confirmed music mode is invalid')
            need(music.get('sound_form') in ('source_mix', 'original_voice_only',
                 'add_music', 'replace_music', 'designed_silence'),
                 'confirmed music direction requires an explicit sound_form')
            need(music.get('dialogue_separation') in ('not_needed', 'required'),
                 'confirmed music direction requires dialogue_separation decision')
            if music.get('dialogue_separation') == 'required':
                need(explicit(music.get('separation_fallback')), 'dialogue separation requires separation_fallback')
        if ready and status == 'confirmed':
            protected = music.get('protected_event_ids', [])
            flexible = music.get('music_flexible_event_ids', [])
            protected = set(protected) if isinstance(protected, list) and all(isinstance(x, str) for x in protected) else set()
            flexible = set(flexible) if isinstance(flexible, list) and all(isinstance(x, str) for x in flexible) else set()
            need((protected | flexible).issubset(events), 'music direction references unknown event IDs')
            need(not protected.intersection(flexible), 'protected events cannot also be music-flexible')
            mode, form = music.get('confirmed_mode'), music.get('sound_form')
            need(type(music.get('music_map_required')) is bool, 'music_map_required must be boolean')
            map_needed = (mode == 'music_led' or bool(flexible) or music.get('music_map_required') is True)
            if map_needed:
                need(music.get('music_map_required') is True, 'music-led/flexible editing requires music_map_required=true')
            asset = music.get('music_asset_ref')
            uses_asset = form in ('add_music', 'replace_music') or map_needed or explicit(asset)
            if form in ('original_voice_only', 'designed_silence'):
                need(not explicit(asset) and not map_needed, 'selected sound_form does not permit a music asset or music-led mapping')
            duration = None
            selection = music.get('music_selection')
            if uses_asset:
                if need(explicit(asset) and (root / asset).is_file(), 'selected music asset is missing'):
                    need(music.get('music_asset_digest') == fingerprint(root / asset), 'selected music asset digest changed or is missing')
                    try:
                        duration = audio_duration(root / asset)
                    except (OSError, ValueError, ZeroDivisionError, subprocess.SubprocessError) as exc:
                        need(False, f'selected music asset cannot be inspected: {exc}')
                if need(isinstance(selection, dict), 'selected music requires music_selection'):
                    for key in ('title', 'version', 'source'):
                        need(explicit(selection.get(key)), f'music_selection requires {key}')
                    a, b = selection.get('start_ms'), selection.get('end_ms')
                    need(type(a) is int and type(b) is int and duration is not None and 0 <= a < b <= duration,
                         'music_selection range must be inside the inspected music asset')
            if form in ('add_music', 'replace_music'):
                tracks = [t for t in timeline.get('audio_tracks', []) if t.get('asset_ref') == asset and explicit(asset)]
                need(bool(tracks), 'selected added/replacement music must appear in final audio_tracks')
                for track in tracks:
                    a, b = track.get('source_in_ms'), track.get('source_out_ms')
                    need(isinstance(selection, dict) and type(a) is int and type(b) is int
                         and type(selection.get('start_ms')) is int and type(selection.get('end_ms')) is int
                         and selection['start_ms'] <= a < b <= selection['end_ms'],
                         'music audio_track range must stay inside the confirmed music selection')
            map_ref = music.get('music_map_ref')
            if map_needed or explicit(map_ref):
                if need(explicit(map_ref) and (root / map_ref).is_file(), 'required music map file is missing'):
                    validate_music_map(read(map_ref, 'music-map'), asset, duration,
                                       selection, events, protected, flexible, need)

    visual_policy = project.get('visual_confirmation_policy')
    if visual_policy is not None:
        need(visual_policy == 'mockup_confirmation_required', 'invalid visual_confirmation_policy')
    visual_ref = project.get('visual_confirmation_ref')
    visual_gate = (project.get('execution_package_policy') == 'plan_and_reference'
                   or visual_policy == 'mockup_confirmation_required' or explicit(visual_ref))
    if visual_gate and ready:
        need(explicit(visual_ref) and (root / visual_ref).is_file(),
             'ready_for_render requires visual-confirmation file and visual_confirmation_ref')
    if explicit(visual_ref) and (root / visual_ref).is_file():
        visual = read(visual_ref, 'visual-confirmation')
        status = visual.get('status')
        need(status in ('draft', 'proposed', 'confirmed'), 'invalid visual-confirmation.status')
        if ready:
            need(status == 'confirmed', 'ready_for_render requires confirmed mockup design')
        if status == 'confirmed':
            identified(visual, 'confirmed mockup design')
            ref = project.get('execution_reference_ref')
            if need(explicit(ref) and (root / ref).is_file(), 'confirmed mockup requires execution reference'):
                need(visual.get('execution_reference_digest') == fingerprint(root / ref),
                     'visual confirmation: execution reference changed since confirmation')
            expected = {k: timeline.get(k) for k in ('width', 'height', 'fps_num', 'fps_den')}
            need(visual.get('output') == expected, 'visual confirmation output specification changed')
            keyframes_ref = project.get('keyframe_references_ref')
            keyframes = {}
            try:
                rows = json.loads((root / keyframes_ref).read_text(encoding='utf-8'))
                keyframes = {r.get('frame_id'): r for r in rows if isinstance(r, dict) and isinstance(r.get('frame_id'), str)}
            except (OSError, ValueError, TypeError):
                need(False, 'confirmed mockup requires original keyframe references')
            mockups = visual.get('mockups')
            if need(isinstance(mockups, list) and bool(mockups), 'confirmed visual design requires actual mockup images'):
                refs, ids = [], []
                for row in mockups:
                    if not need(isinstance(row, dict), 'mockup record must be an object'):
                        continue
                    ids.append(row.get('mockup_id'))
                    need(explicit(row.get('mockup_id')), 'mockup requires mockup_id')
                    need(explicit(row.get('application_scope')), 'mockup requires application_scope')
                    image = row.get('image_ref')
                    refs.append(image)
                    if need(explicit(image) and (root / image).is_file(), 'mockup image is missing'):
                        need(row.get('image_digest') == fingerprint(root / image), 'mockup image changed since visual confirmation')
                        size = image_size(image, 'mockup')
                        need(size == (timeline.get('width'), timeline.get('height')), 'mockup dimensions must match target output')
                    frame_id = row.get('source_frame_id')
                    original = keyframes.get(frame_id, {}) if isinstance(frame_id, str) else {}
                    source_image = original.get('image_ref')
                    if need(original.get('status') == 'available' and explicit(source_image)
                            and (root / source_image).is_file(), 'mockup requires an available original keyframe image'):
                        need(row.get('source_image_digest') == fingerprint(root / source_image),
                             'original keyframe changed since visual confirmation')
                        image_size(source_image, 'original keyframe')
                need(all(isinstance(x, str) for x in ids) and len(ids) == len(set(x for x in ids if isinstance(x, str))), 'mockup IDs must be unique strings')
                assets = project.get('execution_reference_asset_refs', [])
                need(isinstance(assets, list) and len(refs) == len(assets)
                     and all(isinstance(x, str) for x in refs + assets)
                     and sorted(refs) == sorted(assets), 'confirmed mockups must match execution_reference_asset_refs')
    elif visual_gate and not ready:
        warnings.append('Visual confirmation pending; draft/handoff may continue, formal render remains blocked.')
    return errors, warnings


def validate_music_map(data, asset, duration, selection, events, protected, flexible, need):
    need(data.get('analysis_status') in ('complete', 'verified'), 'required music-map must have analysis_status=complete or verified')
    need(data.get('music_asset_ref') == asset and explicit(asset), 'music-map must reference the selected music asset')
    need(type(data.get('duration_ms')) is int and duration is not None and data.get('duration_ms') == duration,
         'music-map duration must match inspected music asset')
    need(explicit(data.get('analysis_method')), 'music-map requires analysis_method')
    qa = data.get('qa')
    need(isinstance(qa, dict) and qa.get('analysis_verified') is True and explicit(qa.get('notes')),
         'music-map requires recorded analysis verification')
    tempo = data.get('tempo_bpm')
    need(tempo is None or type(tempo) in (int, float) and math.isfinite(tempo) and tempo > 0, 'invalid music-map tempo_bpm')
    anchors, times, ranges = set(), [], []
    for key in ('beat_positions_ms', 'accent_positions_ms'):
        values = data.get(key)
        if need(isinstance(values, list), f'music-map.{key} must be an array'):
            valid = all(type(x) is int and duration is not None and 0 <= x < duration for x in values)
            need(valid and values == sorted(set(x for x in values if type(x) is int)), f'music-map.{key} must be ordered unique positions within duration')
            if valid:
                times.extend(values)
    for key in ('sections', 'phrases'):
        rows = data.get(key, [])
        if need(isinstance(rows, list), f'music-map.{key} must be an array'):
            previous_end = 0
            for row in rows:
                if not need(isinstance(row, dict), 'music-map interval must be an object'):
                    continue
                a, b = row.get('start_ms'), row.get('end_ms')
                valid = type(a) is int and type(b) is int and duration is not None and previous_end <= a < b <= duration
                need(valid, 'music-map intervals must be ordered, non-overlapping and within duration')
                identifier = row.get('anchor_id')
                need(explicit(identifier) and identifier not in anchors, 'music-map interval requires unique anchor_id')
                if explicit(identifier):
                    anchors.add(identifier)
                if valid:
                    previous_end = b
                    times.append(a)
                    ranges.append((a, b))
    need(bool(times), 'required music-map must contain editing anchors, not only a complete label')
    if isinstance(selection, dict) and type(selection.get('start_ms')) is int and type(selection.get('end_ms')) is int:
        need(any(selection['start_ms'] <= x < selection['end_ms'] for x in times)
             or any(max(a, selection['start_ms']) < min(b, selection['end_ms']) for a, b in ranges),
             'music-map has no anchor in selected music range')
    mappings = data.get('av_mapping')
    mapped = set()
    if need(isinstance(mappings, list) and bool(mappings), 'music-map requires explicit AV mapping'):
        for row in mappings:
            if not need(isinstance(row, dict), 'AV mapping row must be an object'):
                continue
            eid, relationship = row.get('event_id'), row.get('relationship')
            need(isinstance(eid, str) and eid in events, 'AV mapping references unknown event')
            if isinstance(eid, str):
                mapped.add(eid)
            need(relationship in ('picture_to_music', 'music_to_picture', 'intentional_non_sync'), 'invalid AV mapping relationship')
            need(not isinstance(eid, str) or eid not in protected or relationship != 'picture_to_music', 'protected event cannot be adjusted to a music beat')
            need(type(row.get('sync_tolerance_ms')) is int and row['sync_tolerance_ms'] >= 0, 'AV mapping requires sync_tolerance_ms')
            need(explicit(row.get('reason')), 'AV mapping requires reason')
            if relationship != 'intentional_non_sync':
                need(type(row.get('music_ms')) is int and (row['music_ms'] in times
                     or any(a <= row['music_ms'] < b for a, b in ranges)), 'AV mapping must reference an actual music anchor')
    need(flexible.issubset(mapped), 'music-flexible events must have AV mapping')
