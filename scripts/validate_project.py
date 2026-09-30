#!/usr/bin/env python3
"""Validate core references and timing only; never certifies editorial truth."""
import csv
import json
import math
import sys
from pathlib import Path

from timeline_math import canonical_assembly_ranges, output_ranges_from_overlaps


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


    def load_csv(name):
        path = root / name
        if not path.exists():
            skipped.append(name)
            return [], []
        checked.append(name)
        try:
            with path.open('r', encoding='utf-8-sig', newline='') as fh:
                reader = csv.DictReader(fh)
                headers = reader.fieldnames or []
                rows = list(reader)
            return headers, rows
        except (OSError, csv.Error) as exc:
            errors.append(f'{name}: {exc}')
            return [], []

    def nonblank(value):
        return isinstance(value, str) and bool(value.strip())

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

    project = load('project.json', {})
    structure_state = project.get('structure_state', {}) if isinstance(project, dict) else {}
    broad_complete = isinstance(structure_state, dict) and structure_state.get('broad_pass') in ('complete', 'completed', 'done')
    deep_complete = isinstance(structure_state, dict) and structure_state.get('directed_deep_pass') in ('complete', 'completed', 'done')

    if broad_complete or deep_complete:
        time_policy = project.get('time_policy', {}) if isinstance(project, dict) else {}
        require(isinstance(time_policy, dict) and time_policy.get('time_tag_stability') == 'strict',
                'completed Structure requires strict time_policy.time_tag_stability')
        require(time_policy.get('canonical_source_time_key') == 'source_id+source_ms',
                'completed Structure requires canonical source time key source_id+source_ms')
        require(time_policy.get('require_source_time_mapping') is True,
                'completed Structure requires source time mapping')
        structure_policy = project.get('structure_policy', {}) if isinstance(project, dict) else {}
        require(structure_policy.get('negative_claim_policy') == 'not_observed_is_not_absent',
                'completed Structure requires strict negative-claim policy')
        require(structure_policy.get('negative_claim_dense_sampling_is_sufficient') is False,
                'completed Structure requires dense sampling to be non-sufficient for interval-level absence claims')
        require(structure_policy.get('negative_claim_requires_bounded_scope') is True,
                'completed Structure requires bounded scope for negative claims')
        require(structure_policy.get('negative_claim_requires_fact_type_continuous_or_direct_evidence') is True,
                'completed Structure requires fact-type continuous/direct evidence for negative claims')
        require(structure_policy.get('evidence_conflict_policy') == 'resolve_by_fact_type_and_record_conflict',
                'completed Structure requires fact-type evidence conflict policy')
        require(structure_policy.get('dialect_asr_policy') == 'locator_only_until_verified',
                'completed Structure requires dialect ASR locator-only policy')
        require(structure_policy.get('long_task_checkpoint_policy') == 'incremental_output_resume_coverage',
                'completed Structure requires incremental checkpoint/resume policy')

    sources = index(load('sources.json', []), 'source_id')
    if not sources:
        warnings.append('No source records; this is not an executable media project.')
    for sid, source in sources.items():
        require(positive(source.get('duration_ms')), f'{sid}: duration_ms must be positive integer')
        if not source.get('version'):
            warnings.append(f'{sid}: source version unknown; caches that depend on this source are not reusable')

    def interval(sid, start, end, label):
        if not require(sid in sources, f'{label}: unknown source {sid}'):
            return False
        if not require(integer(start) and integer(end), f'{label}: times must be integer milliseconds'):
            return False
        duration = sources[sid].get('duration_ms')
        return require(positive(duration) and 0 <= start < end <= duration, f'{label}: invalid or out-of-source range')

    if broad_complete:
        for sid, source in sources.items():
            require(isinstance(source.get('time_mapping'), dict) and bool(source.get('time_mapping')),
                    f'{sid}: Broad Structure complete requires explicit time_mapping')
            usable = source.get('usable_ranges')
            if require(isinstance(usable, list) and bool(usable), f'{sid}: Broad Structure complete requires usable_ranges'):
                for i, item in enumerate(usable):
                    label = f'{sid}.usable_ranges[{i}]'
                    if require(isinstance(item, dict), f'{label}: must be object'):
                        interval(sid, item.get('start_ms'), item.get('end_ms'), label)
                        require(nonblank(item.get('reason')), f'{label}: reason must be explicit')
            require(isinstance(source.get('downstream_constraints'), list),
                    f'{sid}: Broad Structure complete requires downstream_constraints array')

    frames = index(load('frames.jsonl', []), 'frame_id')
    if broad_complete:
        require(bool(frames), 'Broad Structure complete requires non-empty frames.jsonl')
        require(structure_state.get('content_map') in ('complete', 'completed', 'done'),
                'Broad Structure complete requires structure_state.content_map=complete')
        scenes = index(load('scenes.jsonl', []), 'scene_id')
        require(bool(scenes), 'Broad Structure complete requires non-empty scenes.jsonl')
        coverage = load('coverage.json', [])
        require(isinstance(coverage, list) and bool(coverage), 'Broad Structure complete requires non-empty coverage.json')
        for i, row in enumerate(coverage):
            label = f'coverage.json[{i}]'
            if not require(isinstance(row, dict), f'{label}: must be object'):
                continue
            interval(row.get('source_id'), row.get('start_ms'), row.get('end_ms'), label)
            require(row.get('modality') in ('visual_sample', 'transcript', 'av_review'), f'{label}: invalid modality')
            require(row.get('status') in ('complete', 'partial', 'failed', 'pending', 'excluded'), f'{label}: invalid status')
            require(nonblank(row.get('method')), f'{label}: method must be explicit')
            require(nonblank(row.get('reason')), f'{label}: reason must be explicit')
        for filename, label in [('overview.md', 'overview.md'), (project.get('content_map_ref') or 'content-map.md', 'content map')]:
            path = root / filename
            require(path.exists() and bool(path.read_text(encoding='utf-8').strip()) if path.exists() else False,
                    f'Broad Structure complete requires non-empty {label}')

    for fid, row in frames.items():
        t = row.get('timestamp_ms')
        interval(row.get('source_id'), t, t + 1 if integer(t) else None, fid)

    if broad_complete:
        complete_values = ('complete', 'completed', 'done')
        for key in ('frame_observations', 'action_node_candidates', 'structure_questions', 'minimum_information_floor'):
            require(structure_state.get(key) in complete_values, f'Broad Structure complete requires structure_state.{key}=complete')
        frame_headers, frame_rows = load_csv('frame-observations.csv')
        required_frame_columns = {
            'source_id', 'timestamp_ms', 'frame_end_ms', 'frame_id', 'frame_name', 'characters',
            'visual_facts', 'visible_action_state', 'observed_emotional_cues', 'expression_gaze',
            'spatial_relationship', 'setting_background', 'key_objects', 'motif_tags', 'visible_text',
            'original_audio_keypoint', 'audio_verification_status', 'nearby_dialogue_refs', 'content_description',
            'change_from_previous', 'topic_judgment', 'confidence', 'confidence_basis', 'unknowns'
        }
        require(required_frame_columns.issubset(set(frame_headers)),
                'frame-observations.csv: missing required minimum-information columns')
        require(bool(frame_rows), 'Broad Structure complete requires non-empty frame-observations.csv')
        observed_ids = []
        for number, row in enumerate(frame_rows, start=2):
            fid = (row.get('frame_id') or '').strip()
            require(bool(fid), f'frame-observations.csv row {number}: missing frame_id')
            if fid:
                observed_ids.append(fid)
            for key in required_frame_columns - {'source_id', 'timestamp_ms', 'frame_id'}:
                require(nonblank(row.get(key)), f'frame-observations.csv row {number}: {key} must be explicit, use none/unknown/not_applicable when empty')
            try:
                t0 = int((row.get('timestamp_ms') or '').strip())
                t1 = int((row.get('frame_end_ms') or '').strip())
            except ValueError:
                t0 = t1 = None
            require(t0 is not None and t1 is not None and t1 > t0, f'frame-observations.csv row {number}: frame_end_ms must be integer > timestamp_ms')
            if fid in frames:
                require((row.get('source_id') or '').strip() == frames[fid].get('source_id'),
                        f'frame-observations.csv row {number}: frame/source time tag mismatch')
                require(t0 == frames[fid].get('timestamp_ms'),
                        f'frame-observations.csv row {number}: timestamp_ms must match frames.jsonl for {fid}')
            allowed_audio_status = {'not_reviewed','subtitle_only','asr_only','audio_verified','no_audio','not_applicable','unknown'}
            require((row.get('audio_verification_status') or '').strip() in allowed_audio_status, f'frame-observations.csv row {number}: invalid audio_verification_status')
        require(set(observed_ids) == set(frames),
                'Broad Structure complete requires frame-observations.csv frame_id set to match frames.jsonl')

        action_headers, action_rows = load_csv('action-node-candidates.csv')
        required_action_columns = {
            'candidate_id', 'source_id', 'trigger_frame_id', 'candidate_start_frame_ref', 'candidate_end_frame_ref',
            'center_timestamp_ms', 'window_start_ms', 'window_end_ms', 'sampling_fps', 'trigger_reason',
            'action_description', 'response_description', 'outcome_description',
            'min_effective_unit_start_ms', 'min_effective_unit_end_ms', 'min_effective_unit_status',
            'lip_sync_check', 'relationship_turn_signal', 'question_refs', 'speaker_adjudication_refs',
            'topic_judgment', 'confidence', 'confidence_basis', 'evidence_refs',
            'verification_status', 'unknowns', 'sampling_exception_reason'
        }
        require(required_action_columns.issubset(set(action_headers)),
                'action-node-candidates.csv: missing required columns')
        for number, row in enumerate(action_rows, start=2):
            label = f'action-node-candidates.csv row {number}'
            require(nonblank(row.get('candidate_id')), f'{label}: missing candidate_id')
            require(nonblank(row.get('trigger_reason')), f'{label}: missing trigger_reason')
            for key in ('candidate_start_frame_ref','candidate_end_frame_ref','action_description','response_description','outcome_description',
                        'min_effective_unit_start_ms','min_effective_unit_end_ms','min_effective_unit_status','lip_sync_check',
                        'relationship_turn_signal','question_refs','speaker_adjudication_refs','topic_judgment','confidence',
                        'confidence_basis','evidence_refs','verification_status','unknowns'):
                require(nonblank(row.get(key)), f'{label}: {key} must be explicit, use none/unknown/not_applicable when empty')
            fps_text = (row.get('sampling_fps') or '').strip()
            try:
                fps = float(fps_text)
            except ValueError:
                fps = None
            require(fps is not None and fps > 0, f'{label}: sampling_fps must be positive')
            sid = (row.get('source_id') or '').strip()
            fid = (row.get('trigger_frame_id') or '').strip()
            require(sid in sources, f'{label}: unknown source_id {sid}')
            require(fid in frames, f'{label}: unknown trigger_frame_id {fid}')
            if fid in frames and sid in sources:
                require(frames[fid].get('source_id') == sid, f'{label}: trigger frame/source mismatch')
            try:
                center = int((row.get('center_timestamp_ms') or '').strip())
                wa = int((row.get('window_start_ms') or '').strip())
                wb = int((row.get('window_end_ms') or '').strip())
            except ValueError:
                center = wa = wb = None
            if sid in sources and center is not None and wa is not None and wb is not None:
                require(0 <= wa <= center < wb <= sources[sid].get('duration_ms', -1), f'{label}: invalid 4fps window range')
                if fid in frames and integer(frames[fid].get('timestamp_ms')):
                    require(wa <= frames[fid]['timestamp_ms'] < wb,
                            f'{label}: trigger frame timestamp must fall inside candidate window')
            else:
                require(False, f'{label}: center/window times must be integer milliseconds')
            if fps is not None and abs(fps - 4.0) > 1e-9:
                require(nonblank(row.get('sampling_exception_reason')), f'{label}: non-4fps window requires sampling_exception_reason')

        question_headers, question_rows = load_csv('structure-questions.csv')
        required_question_columns = {
            'question_id', 'stage', 'question', 'answer', 'answer_status', 'evidence_refs',
            'confidence', 'confidence_basis', 'unverified_items', 'next_check'
        }
        require(required_question_columns.issubset(set(question_headers)),
                'structure-questions.csv: missing required columns')
        allowed_status = {'supported', 'partial', 'unresolved', 'contradicted', 'not_applicable'}
        for number, row in enumerate(question_rows, start=2):
            label = f'structure-questions.csv row {number}'
            require(nonblank(row.get('question_id')), f'{label}: missing question_id')
            require(nonblank(row.get('question')), f'{label}: missing question')
            require((row.get('answer_status') or '').strip() in allowed_status, f'{label}: invalid answer_status')
            require(nonblank(row.get('answer')), f'{label}: answer must be explicit, use unresolved when not answered')
            require(nonblank(row.get('confidence')), f'{label}: confidence must be explicit')
            require(nonblank(row.get('confidence_basis')), f'{label}: confidence_basis must be explicit')
            require(nonblank(row.get('evidence_refs')), f'{label}: evidence_refs must be explicit, use none when empty')
            require(nonblank(row.get('unverified_items')), f'{label}: unverified_items must be explicit, use none when empty')
            require(nonblank(row.get('next_check')), f'{label}: next_check must be explicit, use none when no follow-up is needed')

    transcript = index(load('transcript.jsonl', []), 'utterance_id')
    for tid, row in transcript.items():
        interval(row.get('source_id'), row.get('start_ms'), row.get('end_ms'), tid)
        require(isinstance(row.get('audio_verified'), bool), f'{tid}: audio_verified must be boolean')
        if row.get('origin') == 'asr':
            require(row.get('asr_role') in ('locator_only', 'candidate', 'verified_transcript'),
                    f'{tid}: ASR utterance requires explicit asr_role')
            if row.get('asr_role') == 'verified_transcript':
                require(row.get('audio_verified') is True or bool(row.get('review_refs')),
                        f'{tid}: verified_transcript ASR requires audio/review evidence')

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

    def ranges_cover(ranges, start, end):
        """Return True when half-open integer ranges fully cover [start, end)."""
        cursor = start
        for a, b in sorted(ranges):
            if b <= cursor:
                continue
            if a > cursor:
                break
            cursor = max(cursor, b)
            if cursor >= end:
                return True
        return cursor >= end

    units = index(load('units.jsonl', []), 'unit_id')
    # Always initialize Deep evidence indexes so incomplete stage state produces
    # normal validation errors instead of UnboundLocalError later in preflight.
    deep_index = {}
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

    if deep_complete:
        complete_values = ('complete', 'completed', 'done')
        require(structure_state.get('deep_observations') in complete_values, 'Directed Deep Structure complete requires structure_state.deep_observations=complete')
        require(structure_state.get('detail_intervals') in complete_values, 'Directed Deep Structure complete requires structure_state.detail_intervals=complete')
        require(structure_state.get('speaker_adjudications') in complete_values, 'Directed Deep Structure complete requires structure_state.speaker_adjudications=complete')

        detail_headers, detail_rows = load_csv('detail-intervals.csv')
        required_detail_columns = {
            'detail_interval_id','plan_node_id','source_id','start_ms','end_ms','entry_reason','preceding_context',
            'current_background','following_context','content_summary','target_questions','topic_relevance',
            'evidence_refs','unknowns'
        }
        require(required_detail_columns.issubset(set(detail_headers)), 'detail-intervals.csv: missing required detailed-context columns')
        require(bool(detail_rows), 'Directed Deep Structure complete requires at least one detail interval')
        for number, row in enumerate(detail_rows, start=2):
            label=f'detail-intervals.csv row {number}'
            for key in required_detail_columns - {'start_ms','end_ms'}:
                require(nonblank(row.get(key)), f'{label}: {key} must be explicit, use none/unknown/not_applicable when empty')
            sid=(row.get('source_id') or '').strip()
            try:
                a=int((row.get('start_ms') or '').strip()); b=int((row.get('end_ms') or '').strip())
            except ValueError:
                a=b=None
            if a is None or b is None:
                require(False, f'{label}: start_ms/end_ms must be integer milliseconds')
            else:
                interval(sid,a,b,label)

        detail_index = {(r.get('detail_interval_id') or '').strip(): r for r in detail_rows}

        speaker_headers, speaker_rows = load_csv('speaker-adjudications.csv')
        required_speaker_columns = {
            'adjudication_id','stage','source_id','utterance_id','start_ms','end_ms','frame_window_refs',
            'lip_movement_observation','visible_speaker_candidate','addressee_candidate','audio_speaker_candidate',
            'hard_subtitle_signal','asr_signal','asr_role','evidence_resolution_rule','subtitle_audio_conflict',
            'decision','decision_basis','confidence','evidence_refs','unknowns'
        }
        require(required_speaker_columns.issubset(set(speaker_headers)), 'speaker-adjudications.csv: missing required speaker-adjudication columns')
        for number, row in enumerate(speaker_rows, start=2):
            label=f'speaker-adjudications.csv row {number}'
            for key in required_speaker_columns - {'start_ms','end_ms'}:
                require(nonblank(row.get(key)), f'{label}: {key} must be explicit, use none/unknown/not_applicable when empty')
            sid=(row.get('source_id') or '').strip()
            try:
                a=int((row.get('start_ms') or '').strip()); b=int((row.get('end_ms') or '').strip())
            except ValueError:
                a=b=None
            if a is None or b is None:
                require(False, f'{label}: start_ms/end_ms must be integer milliseconds')
            else:
                interval(sid,a,b,label)
            tid = (row.get('utterance_id') or '').strip()
            if require(tid in transcript, f'{label}: unknown utterance_id {tid}'):
                utterance = transcript[tid]
                require(utterance.get('source_id') == sid, f'{label}: utterance/source time tag mismatch')
                ua, ub = utterance.get('start_ms'), utterance.get('end_ms')
                if a is not None and b is not None and integer(ua) and integer(ub):
                    require(max(a, ua) < min(b, ub), f'{label}: adjudication range must overlap utterance range')
            require((row.get('asr_role') or '').strip() in ('locator_only_until_verified','candidate','verified'),
                    f'{label}: invalid asr_role')
            require((row.get('evidence_resolution_rule') or '').strip() == 'resolve_by_fact_type_and_record_conflict',
                    f'{label}: evidence_resolution_rule must preserve fact-type conflict resolution')
            allowed_decisions={'resolved','supported','partial','unresolved','contradicted','not_applicable'}
            require((row.get('decision') or '').strip() in allowed_decisions, f'{label}: invalid decision')

        deep_headers, deep_rows = load_csv('deep-observations.csv')
        required_deep_columns = {
            'observation_id', 'detail_interval_id', 'plan_node_id', 'source_id', 'start_ms', 'end_ms', 'visual_facts',
            'action_chain', 'key_visual_changes', 'observed_emotional_cues', 'emotional_interpretation',
            'setting_context', 'narrative_context', 'motif_tags', 'content_description', 'hard_subtitle_notes',
            'original_audio_keypoints', 'audio_verification_status', 'subtitle_asr_conflicts', 'dialogue_audio',
            'speaker_adjudication_refs', 'before_state', 'after_state', 'question_refs', 'topic_judgment',
            'confidence', 'confidence_basis', 'interpretations', 'unknowns', 'unverified_items',
            'evidence_status', 'counterevidence', 'context_ranges', 'protected_ranges', 'min_effective_unit_candidate'
        }
        require(required_deep_columns.issubset(set(deep_headers)),
                'deep-observations.csv: missing required detailed-structure columns')
        require(bool(deep_rows), 'Directed Deep Structure complete requires at least one deep observation')
        for number, row in enumerate(deep_rows, start=2):
            label = f'deep-observations.csv row {number}'
            observation_id = (row.get('observation_id') or '').strip()
            if require(bool(observation_id), f'{label}: observation_id must be explicit'):
                require(observation_id not in deep_index, f'{label}: duplicate observation_id {observation_id}')
                deep_index[observation_id] = row
            for key in ('observation_id', 'detail_interval_id', 'plan_node_id', 'visual_facts', 'shot_composition',
                        'action_chain', 'key_visual_changes', 'observed_emotional_cues', 'emotional_interpretation',
                        'expression_gaze', 'spatial_relationship', 'setting_context', 'narrative_context', 'motif_tags',
                        'content_description', 'hard_subtitle_notes', 'original_audio_keypoints', 'audio_verification_status',
                        'subtitle_asr_conflicts', 'dialogue_audio', 'speaker_adjudication_refs', 'before_state', 'after_state',
                        'question_refs', 'topic_judgment', 'confidence', 'confidence_basis', 'interpretations',
                        'unknowns', 'unverified_items', 'evidence_status', 'counterevidence', 'context_ranges',
                        'protected_ranges', 'min_effective_unit_candidate', 'isolated_use_risk', 'review_refs',
                        'narrative_function', 'edit_note'):
                require(nonblank(row.get(key)), f'{label}: {key} must be explicit, use none/unknown/not_applicable when empty')
            sid=(row.get('source_id') or '').strip()
            try:
                a=int((row.get('start_ms') or '').strip()); b=int((row.get('end_ms') or '').strip())
            except ValueError:
                a=b=None
            if a is None or b is None:
                require(False, f'{label}: start_ms/end_ms must be integer milliseconds')
            else:
                interval(sid,a,b,label)
            detail_id = (row.get('detail_interval_id') or '').strip()
            if require(detail_id in detail_index, f'{label}: unknown detail_interval_id'):
                detail = detail_index[detail_id]
                require((detail.get('source_id') or '').strip() == sid, f'{label}: detail/source time tag mismatch')
                try:
                    da = int((detail.get('start_ms') or '').strip()); db = int((detail.get('end_ms') or '').strip())
                except ValueError:
                    da = db = None
                if a is not None and b is not None and da is not None and db is not None:
                    require(da <= a < b <= db, f'{label}: deep observation must stay inside its detail interval')
            require((row.get('evidence_status') or '').strip() in ('pending', 'supported', 'contradicted', 'partial'),
                    f'{label}: invalid evidence_status')

    timeline = load('timeline.json', {})
    events = timeline.get('events', [])
    if not require(isinstance(events, list), 'timeline.events must be array'):
        events = []
    event_index = index(events, 'event_id')
    ready = timeline.get('status') == 'ready_for_render'
    if ready:
        require(bool(events), 'ready_for_render has no events')
        require(positive(timeline.get('width')) and positive(timeline.get('height')), 'ready_for_render requires output dimensions')
        complete_values = ('complete', 'completed', 'done')
        require(structure_state.get('broad_pass') in complete_values and structure_state.get('content_map') in complete_values,
                'ready_for_render requires completed Broad Structure + Content Map')
        require(structure_state.get('directed_deep_pass') in complete_values,
                'ready_for_render requires completed Directed Deep / Detail Structure')
        require(project.get('narrative_direction_status') == 'confirmed',
                'ready_for_render requires narrative_direction_status=confirmed')
        require(project.get('execution_plan_status') == 'confirmed',
                'ready_for_render requires execution_plan_status=confirmed')
        for key, label in [('narrative_direction_ref', 'Narrative Direction'), ('execution_plan_ref', 'Editorial Execution Plan')]:
            ref = project.get(key)
            if require(nonblank(ref), f'ready_for_render requires {key}'):
                path = root / ref
                require(path.exists() and bool(path.read_text(encoding='utf-8').strip()) if path.exists() else False,
                        f'ready_for_render requires non-empty {label} file: {ref}')
        require(project.get('render_authorized') is True, 'ready_for_render requires render_authorized=true')
        time_policy = project.get('time_policy', {}) if isinstance(project, dict) else {}
        require(isinstance(time_policy, dict) and time_policy.get('time_tag_stability') == 'strict',
                'ready_for_render requires strict time-tag policy')
        execution_policy = project.get('execution_policy', {}) if isinstance(project, dict) else {}
        require(execution_policy.get('duration_budget_required_before_ready') is True,
                'ready_for_render requires duration budget policy')
        require(execution_policy.get('feedback_invalidation_matrix') == 'strict',
                'ready_for_render requires feedback invalidation policy')
        require(execution_policy.get('audio_narrative_role_required') is True,
                'ready_for_render requires audio narrative-role policy')
    fps_num, fps_den = timeline.get('fps_num'), timeline.get('fps_den')
    fps_ok = positive(fps_num) and positive(fps_den)
    if events:
        require(fps_ok, 'timeline requires positive integer fps_num/fps_den')
    frame_ms = 1000 * fps_den / fps_num if fps_ok else None
    canonical_ranges = []
    if events and fps_ok:
        try:
            canonical_ranges = canonical_assembly_ranges(events, fps_num, fps_den)
        except ValueError as exc:
            require(False, f'timeline cumulative quantization: {exc}')
            canonical_ranges = []
    canonical_by_id = {}
    for i, event in enumerate(event_index.values()):
        eid = event['event_id']
        a, b = event.get('out_in_frame'), event.get('out_out_frame')
        out_ok = integer(a) and integer(b) and 0 <= a < b
        require(out_ok, f'{eid}: invalid assembly frame range')
        if i < len(canonical_ranges):
            expected = canonical_ranges[i]
            canonical_by_id[eid] = expected
            require(a == expected['assembly_in_frame'] and b == expected['assembly_out_frame'],
                    f'{eid}: assembly range must use cumulative timeline quantization; expected '
                    f"{expected['assembly_in_frame']}-{expected['assembly_out_frame']}")
        kind = event.get('kind')
        require(kind in ('source', 'card'), f'{eid}: unsupported event kind')
        if kind != 'source':
            continue
        sid = event.get('source_id')
        start_ms, end_ms = event.get('source_in_ms'), event.get('source_out_ms')
        valid = interval(sid, start_ms, end_ms, eid)
        speed = event.get('speed', 1)
        speed_ok = type(speed) in (int, float) and math.isfinite(speed) and speed > 0
        require(speed_ok, f'{eid}: invalid speed')
        uid = event.get('unit_id')
        if not require(isinstance(uid, str) and uid in units, f'{eid}: unknown unit {uid}'):
            continue
        unit = units[uid]
        require(unit.get('source_id') == sid, f'{eid}: unit/source mismatch')
        if valid and integer(unit.get('start_ms')) and integer(unit.get('end_ms')):
            require(unit['start_ms'] <= start_ms < end_ms <= unit['end_ms'], f'{eid}: cut outside unit')
            for p in unit.get('protected_ranges', []):
                if isinstance(p, dict) and integer(p.get('start_ms')) and integer(p.get('end_ms')):
                    require(start_ms <= p['start_ms'] < p['end_ms'] <= end_ms, f'{eid}: cut drops protected meaning range')
        if ready:
            require(bool(sources.get(sid, {}).get('version')), f'{eid}: source version must be known')
            require(isinstance(sources.get(sid, {}).get('time_mapping'), dict) and bool(sources.get(sid, {}).get('time_mapping')),
                    f'{eid}: ready source requires explicit time_mapping')
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
                            require(covered_review(valid_refs, sid, start_ms, end_ms, modality), f'{uid}: {modality} review does not cover selected range')
                for name in ('audio', 'visual', 'context'):
                    if verification.get(name) == 'not_applicable':
                        reasons = verification.get('not_applicable_reasons', {})
                        require(isinstance(reasons, dict) and bool(reasons.get(name)), f'{uid}: missing reason for {name} not_applicable')
            require(bool(unit.get('protected_ranges')) or bool(unit.get('protection_note')), f'{uid}: missing protection decision')

    transitions = load('transitions.json', [])
    event_ids = list(event_index)
    pairs = list(zip(event_ids[:-1], event_ids[1:]))
    seen = []
    overlap_by_pair = {}
    relations = {'continuous', 'ellipsis', 'comparison', 'flashback', 'chapter_change'}
    for row in transitions:
        if not require(isinstance(row, dict), 'transition must be object'):
            continue
        pair = (row.get('from_event'), row.get('to_event'))
        require(pair in pairs, f'transition {pair}: not adjacent events')
        require(pair not in seen, f'transition {pair}: duplicate')
        seen.append(pair)
        require(row.get('relation') in relations, f'transition {pair}: invalid relation')
        overlap = row.get('overlap_frames', 0)
        if require(integer(overlap) and overlap >= 0, f'transition {pair}: overlap_frames must be nonnegative integer'):
            effect = row.get('effect', 'hard_cut')
            require(effect in ('hard_cut', 'xfade'), f'transition {pair}: invalid effect')
            require(not (effect == 'hard_cut' and overlap) and not (effect == 'xfade' and overlap == 0),
                    f'transition {pair}: hard_cut requires zero overlap; xfade requires positive overlap')
            overlap_by_pair[pair] = overlap
    if events:
        require(set(seen) == set(pairs), 'every adjacent event pair needs a transition record')

    output_ranges = []
    total_output = 0
    overlaps = [0] + [overlap_by_pair.get(pair, 0) for pair in pairs] if events else []
    if canonical_ranges and len(overlaps) == len(canonical_ranges):
        try:
            output_ranges, total_output = output_ranges_from_overlaps(canonical_ranges, overlaps)
        except ValueError as exc:
            require(False, f'timeline output mapping: {exc}')
            output_ranges, total_output = [], 0
    output_by_id = {eid: output_ranges[i] for i, eid in enumerate(event_ids) if i < len(output_ranges)}

    if ready:
        budget = timeline.get('duration_budget', {})
        if require(isinstance(budget, dict), 'ready_for_render requires timeline.duration_budget object') and canonical_ranges:
            sum_event_frames = sum(r['length_frames'] for r in canonical_ranges)
            sum_overlap_frames = sum(overlaps)
            require(budget.get('sum_event_frames') == sum_event_frames,
                    'duration_budget.sum_event_frames must equal cumulative-quantized event frames')
            require(budget.get('sum_transition_overlap_frames') == sum_overlap_frames,
                    'duration_budget.sum_transition_overlap_frames must equal transition overlaps')
            require(budget.get('computed_output_frames') == total_output,
                    'duration_budget.computed_output_frames must equal compiled output frames')
            target = budget.get('target_max_frames')
            target_ms = project.get('target_duration_ms') if isinstance(project, dict) else None
            if target_ms is not None and fps_ok:
                derived_target = math.floor(target_ms * fps_num / (1000 * fps_den))
                require(target == derived_target, 'duration_budget.target_max_frames must match project target_duration_ms')
            if target is None:
                require(budget.get('status') == 'checked_no_limit',
                        'duration budget without target must use status=checked_no_limit')
            elif require(integer(target) and target > 0, 'duration_budget.target_max_frames must be positive integer or null'):
                require(total_output <= target, 'ready_for_render exceeds target duration budget')
                require(budget.get('status') == 'within_budget',
                        'duration budget with target must use status=within_budget')

        # Each selected source event must explicitly name the Deep observations actually used.
        # Only run evidence-linkage checks after Directed Deep / Detail is complete.
        # If the stage is pending, the ready_for_render stage gate above is the structured
        # error; do not cascade into unknown-evidence errors or crash on an unbuilt index.
        if deep_complete:
            evidence_events = events
        else:
            evidence_events = []
        # Do not gate an event on every observation that happens to share the same unit_id:
        # unused pending/contradicted observations remain valid evidence records but are not blockers.
        for event in evidence_events:
            if event.get('kind') != 'source':
                continue
            eid = event.get('event_id') or 'source event'
            sid = event.get('source_id')
            start_ms, end_ms = event.get('source_in_ms'), event.get('source_out_ms')
            refs = event.get('deep_observation_refs')
            if not require(isinstance(refs, list) and bool(refs),
                           f'{eid}: selected source event requires non-empty deep_observation_refs'):
                continue
            string_refs = [ref for ref in refs if isinstance(ref, str)]
            require(len(string_refs) == len(refs), f'{eid}: deep_observation_refs must contain only strings')
            require(len(string_refs) == len(set(string_refs)), f'{eid}: duplicate deep_observation_refs')
            support_ranges = []
            for ref in string_refs:
                if not require(ref in deep_index, f'{eid}: unknown Deep observation {ref}'):
                    continue
                row = deep_index[ref]
                require((row.get('source_id') or '').strip() == sid,
                        f'{eid}: Deep observation {ref} source mismatch')
                status = (row.get('evidence_status') or '').strip()
                require(status in ('supported', 'partial'),
                        f'{eid}: Deep observation {ref} evidence_status must be supported/partial, got {status or "blank"}')
                try:
                    a = int((row.get('start_ms') or '').strip())
                    b = int((row.get('end_ms') or '').strip())
                except ValueError:
                    a = b = None
                if a is not None and b is not None and integer(start_ms) and integer(end_ms):
                    require(max(a, start_ms) < min(b, end_ms),
                            f'{eid}: Deep observation {ref} does not overlap selected source range')
                    support_ranges.append((max(a, start_ms), min(b, end_ms)))
            if integer(start_ms) and integer(end_ms):
                require(ranges_cover(support_ranges, start_ms, end_ms),
                        f'{eid}: referenced Deep observations do not fully cover selected source range')

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
                anchor_id = row['anchor_event_id']
                anchor = output_by_id.get(anchor_id)
                if require(anchor is not None, f'{label}: unknown event anchor'):
                    la, lb = row.get('local_in_frame'), row.get('local_out_frame')
                    if require(integer(la) and integer(lb) and lb > la, f'{label}: local frames must be increasing integers'):
                        a, b = anchor['out_in_frame'] + la, anchor['out_in_frame'] + lb
            else:
                require(row.get('coordinate_space') == 'output',
                        f'{label}: absolute track timing requires coordinate_space=output')
            require(integer(a) and integer(b) and 0 <= a < b <= total_output, f'{label}: outside compiled output')
            if key == 'audio_tracks':
                if row.get('source_id'):
                    interval(row['source_id'], row.get('source_in_ms'), row.get('source_out_ms'), label)
                if ready:
                    require(row.get('narrative_role') in ('dialogue_information','ambience_continuity','emotional_music','rhythm_cue','intentional_silence','other'),
                            f'{label}: ready audio track requires narrative_role')
                    require(nonblank(row.get('treatment_reason')), f'{label}: ready audio track requires treatment_reason')

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
