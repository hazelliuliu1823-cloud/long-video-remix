"""Exercise cross-model package declarations and stale-reference protection.

Fixtures are synthetic records; no video, typography or visual QA is certified.
"""
import json
import base64
import hashlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / 'scripts'))
from check_render_authorization import check
from compile_render_manifest import compile_manifest
from execution_integrity import digest
from prepare_execution_authorization import prepare
from validate_project import validate
from test_execution_integrity import write_fixture


class ExecutionPackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.files = json.loads((PACKAGE / 'tests/fixtures/ready-project.json').read_text())
        self.files['project.json'].update(
            execution_package_policy='plan_and_reference',
            structure_exceptions_ref='structure-exceptions.jsonl',
            keyframe_references_ref='keyframe-references.json',
            execution_handoff_ref='execution-handoff.md',
            execution_reference_ref='execution-reference.md',
            execution_reference_asset_refs=[],
            music_direction_policy='mode_confirmation_required',
            music_direction_ref='music-direction.json',
            visual_confirmation_policy='mockup_confirmation_required',
            visual_confirmation_ref='visual-confirmation.json',
            capability_resolution_policy='discover_then_prepare_if_permitted')
        self.files['execution-handoff.md'] = 'Synthetic handoff with source evidence and downstream package requirements.\n'
        self.files['execution-reference.md'] = 'Synthetic confirmed production rules; images are synthetic fixtures, not real source evidence.\n'
        self.files['music-direction.json'] = {
            'schema_version': '1.0', 'decision_id': 'MD001', 'status': 'confirmed',
            'proposed_mode': 'hybrid', 'proposed_by': 'synthetic-director',
            'basis_refs': ['narrative-direction.md', 'execution-handoff.md'],
            'recommendation_reason': 'Synthetic narrative anchors are fixed while one region is rhythm-flexible.',
            'protected_event_ids': ['E001'], 'music_flexible_event_ids': [],
            'music_asset_ref': None, 'music_map_required': False, 'music_map_ref': None,
            'sound_form': 'source_mix', 'dialogue_separation': 'not_needed', 'separation_fallback': None,
            'confirmation_source': 'synthetic test instruction', 'confirmed_mode': 'narrative_led',
            'confirmed_by': 'synthetic-test-author', 'confirmed_at': '2026-10-14'}
        self.files['keyframe-references.json'] = [{
            'frame_id': 'F001', 'source_id': 'SRC001', 'timestamp_ms': 1000,
            'image_ref': None, 'source_segment': 'U001', 'narrative_role': 'opening',
            'notes': 'Image export is unavailable; source evidence remains in existing records.',
            'status': 'unavailable', 'reason': 'This environment cannot export a frame image.',
            'impact': 'low', 'downstream_handling': 'Continue with explicit production parameters; do not claim an image preview.'}]
        dimensions = tuple(self.files['timeline.json'][k] for k in ('width', 'height'))
        buffer = io.BytesIO()
        Image.new('RGB', dimensions, '#284862').save(buffer, format='PNG')
        self.binary_files = {'keyframe-visual.png': buffer.getvalue(), 'mockup.png': buffer.getvalue()}
        self.files['keyframe-references.json'].append({
            'frame_id': 'F-VISUAL', 'source_id': 'SRC001', 'timestamp_ms': 1000,
            'image_ref': 'keyframe-visual.png', 'source_segment': 'U001', 'narrative_role': 'style',
            'notes': 'Synthetic original frame stand-in for automated checks only.',
            'status': 'available', 'reason': None, 'impact': None, 'downstream_handling': None})
        self.files['project.json']['execution_reference_asset_refs'] = ['mockup.png']
        self.files['visual-confirmation.json'] = {
            'schema_version': '1.0', 'decision_id': 'VD-SYNTHETIC', 'status': 'confirmed',
            'confirmed_by': 'synthetic-test-author', 'confirmed_at': '2026-10-14',
            'confirmation_source': 'synthetic test instruction approves this fixture and these rules',
            'execution_reference_digest': hashlib.sha256(self.files['execution-reference.md'].encode()).hexdigest(),
            'output': {k: self.files['timeline.json'][k] for k in ('width', 'height', 'fps_num', 'fps_den')},
            'mockups': [{'mockup_id': 'M01', 'image_ref': 'mockup.png',
                'image_digest': hashlib.sha256(buffer.getvalue()).hexdigest(),
                'source_frame_id': 'F-VISUAL', 'source_image_digest': hashlib.sha256(buffer.getvalue()).hexdigest(),
                'application_scope': 'all synthetic events'}]}
        self.files['structure-exceptions.jsonl'] = [{
            'exception_id': 'EX001', 'stage': 'E', 'artifact': 'keyframe-references.json',
            'record_id': 'F001', 'field': 'image_ref', 'status': 'unavailable',
            'reason': 'This environment cannot export a frame image.', 'impact': 'low',
            'downstream_handling': 'Carry the gap into the handoff and use specified production rules.'}]
        self.save()

    def save(self, confirm=True):
        write_fixture(self.root, self.files)
        for name, data in self.binary_files.items():
            (self.root / name).write_bytes(data)
        if confirm:
            # Only this test author confirms its own synthetic decision.
            auth = prepare(self.root)
            auth.update(status='confirmed', confirmed_by='synthetic-test-author',
                        authorization_id='AUTH-PACKAGE-SYNTHETIC')
            (self.root / 'execution-authorization.json').write_text(json.dumps(auth))
            project = self.files['project.json'].copy()
            project['execution_authorization_digest'] = digest(auth)
            (self.root / 'project.json').write_text(json.dumps(project))

    def assert_blocked(self, message):
        report = validate(self.root)
        self.assertEqual(report['status'], 'fail', report)
        self.assertTrue(any(message in x for x in report['errors']), report['errors'])
        with self.assertRaises(ValueError):
            compile_manifest(self.root)

    def test_image_export_exception_continues_without_weakening_render_checks(self):
        report = validate(self.root)
        self.assertEqual(report['status'], 'pass', report['errors'])
        self.assertTrue(any('unavailable' in x for x in report['warnings']))
        self.assertTrue(compile_manifest(self.root)['render_allowed'])

    def test_capability_resolution_policy_accepts_prepare_if_permitted(self):
        report = validate(self.root)
        self.assertEqual(report['status'], 'pass', report['errors'])

    def test_invalid_capability_resolution_policy_is_blocked(self):
        self.files['project.json']['capability_resolution_policy'] = 'silent_install_everything'
        self.save()
        self.assert_blocked('invalid capability_resolution_policy')

    def test_missing_handoff_blocks_false_detail_completion(self):
        (self.root / 'execution-handoff.md').unlink()
        self.assert_blocked('execution-handoff.md')

    def test_missing_reference_blocks_new_package_execution(self):
        (self.root / 'execution-reference.md').unlink()
        self.assert_blocked('execution reference document')

    def test_music_mode_must_be_confirmed_before_ready(self):
        self.files['music-direction.json'].update(status='proposed', confirmed_mode=None,
                                                  confirmed_by=None, confirmation_source=None)
        self.save()
        self.assert_blocked('confirmed music mode')

    def test_missing_music_direction_blocks_new_policy(self):
        (self.root / 'music-direction.json').unlink()
        self.assert_blocked('music direction file')

    def test_music_direction_ref_without_policy_still_requires_confirmation(self):
        self.files['project.json'].pop('music_direction_policy', None)
        self.files['music-direction.json'].update(status='proposed', confirmed_mode=None,
                                                  confirmed_by=None, confirmation_source=None)
        self.save()
        self.assert_blocked('confirmed music mode')

    def test_changed_music_direction_invalidates_confirmation(self):
        manifest = compile_manifest(self.root)
        decision = json.loads((self.root / 'music-direction.json').read_text())
        decision['confirmed_mode'] = 'narrative_led'
        (self.root / 'music-direction.json').write_text(json.dumps(decision))
        self.assert_blocked('music_direction_ref changed since confirmation')
        with self.assertRaises(ValueError):
            check(self.root, manifest)

    def test_required_music_map_must_exist_and_be_complete(self):
        self.add_music_map()
        self.files['music-map.json']['analysis_status'] = 'pending'
        self.save()
        self.assert_blocked('required music-map must have analysis_status=complete or verified')
        self.files['music-map.json']['analysis_status'] = 'complete'
        self.save()
        self.assertEqual(validate(self.root)['status'], 'pass')

    def test_changed_music_map_invalidates_confirmation_and_old_manifest(self):
        self.add_music_map()
        self.save()
        manifest = compile_manifest(self.root)
        music_map = json.loads((self.root / 'music-map.json').read_text())
        music_map['beat_positions_ms'] = [500, 1000]
        (self.root / 'music-map.json').write_text(json.dumps(music_map))
        self.assert_blocked('music map changed since confirmation')
        with self.assertRaises(ValueError):
            check(self.root, manifest)

    def test_changed_reference_invalidates_confirmation_and_old_manifest(self):
        manifest = compile_manifest(self.root)
        (self.root / 'execution-reference.md').write_text('Changed style decision without reconfirmation.\n')
        self.assert_blocked('execution_reference_ref changed since confirmation')
        with self.assertRaises(ValueError):
            check(self.root, manifest)

    def test_style_asset_change_invalidates_confirmation(self):
        manifest = compile_manifest(self.root)
        (self.root / 'mockup.png').write_bytes(self.binary_files['mockup.png'] + b'changed')
        self.assert_blocked('reference assets changed since confirmation')
        with self.assertRaises(ValueError):
            check(self.root, manifest)

    def test_missing_mockup_blocks_formal_render(self):
        self.files['project.json']['execution_reference_asset_refs'] = []
        self.files['visual-confirmation.json']['mockups'] = []
        self.save()
        self.assert_blocked('requires actual')

    def test_declared_nonimage_cannot_replace_a_mockup(self):
        self.files['mockup-01.dat'] = 'Synthetic mockup placeholder bytes.\n'
        self.files['project.json']['execution_reference_asset_refs'] = ['mockup-01.dat']
        self.files['visual-confirmation.json']['mockups'][0].update(image_ref='mockup-01.dat',
            image_digest=hashlib.sha256(self.files['mockup-01.dat'].encode()).hexdigest())
        self.save()
        self.assert_blocked('readable image required')

    def test_missing_exception_reason_is_not_silently_accepted(self):
        self.files['structure-exceptions.jsonl'][0]['reason'] = ''
        self.save()
        self.assert_blocked('reason must be explicit')

    def test_unknown_keyframe_time_is_null_and_does_not_stop_independent_work(self):
        self.files['keyframe-references.json'][0]['timestamp_ms'] = None
        self.save()
        self.assertEqual(validate(self.root)['status'], 'pass')

    def test_empty_keyframe_list_requires_an_artifact_exception(self):
        self.files['keyframe-references.json'] = []
        self.save()
        self.assert_blocked('empty keyframe references')
        self.files['structure-exceptions.jsonl'][0].update(record_id=None, field='*')
        self.files['timeline.json']['status'] = 'draft'
        self.files['project.json']['render_authorized'] = False
        self.files['visual-confirmation.json']['status'] = 'proposed'
        self.save()
        self.assertEqual(validate(self.root)['status'], 'pass')
        self.assertFalse(compile_manifest(self.root, planning=True)['render_allowed'])

    def test_exception_does_not_release_unverified_adopted_evidence(self):
        self.files['deep-observations.csv']['rows'][0]['evidence_status'] = 'pending'
        self.save()
        self.assert_blocked('evidence')

    def test_available_keyframe_cannot_point_to_a_nonexistent_image(self):
        self.files['keyframe-references.json'][0].update(status='available', image_ref='missing.png')
        self.save()
        self.assert_blocked('available image file is missing')

    def test_preparation_stays_a_draft_with_reference_dependencies(self):
        auth = prepare(self.root)
        self.assertEqual(auth['status'], 'draft')
        self.assertIsNone(auth['confirmed_by'])
        self.assertTrue(auth['execution_reference_digest'])
        self.assertIn('mockup.png', auth['execution_reference_asset_digests'])
        self.assertTrue(auth['visual_confirmation_digest'])

    def add_music_map(self):
        import wave
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as stream:
            stream.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
            stream.writeframes(b'\x00\x00' * 80000)
        self.binary_files['music.wav'] = buffer.getvalue()
        self.files['music-direction.json'].update(music_map_required=True, music_map_ref='music-map.json',
            music_asset_ref='music.wav', music_asset_digest=hashlib.sha256(buffer.getvalue()).hexdigest(),
            music_selection={'title': 'synthetic silence', 'version': 'fixture-v1', 'source': 'authored test data',
                             'start_ms': 0, 'end_ms': 10000})
        self.files['music-map.json'] = {
            'schema_version': '1.0', 'music_asset_ref': 'music.wav', 'analysis_method': 'synthetic authored anchors',
            'analysis_status': 'complete', 'duration_ms': 10000, 'tempo_bpm': 120,
            'beat_positions_ms': [500], 'accent_positions_ms': [], 'energy_curve': [], 'sections': [], 'phrases': [],
            'editorial_notes': ['Synthetic fixture; not an actual music analysis.'],
            'av_mapping': [{'event_id': 'E001', 'music_ms': 500, 'sync_tolerance_ms': 40,
                            'relationship': 'music_to_picture', 'reason': 'Preserve the protected narrative event.'}],
            'qa': {'analysis_verified': True, 'notes': 'Synthetic test author checks this declared fixture only.'}}

    def test_visual_confirmation_file_is_required(self):
        (self.root / 'visual-confirmation.json').unlink()
        self.assert_blocked('requires visual-confirmation file')

    def test_package_policy_cannot_skip_visual_confirmation(self):
        self.files['project.json'].pop('visual_confirmation_policy')
        self.files['project.json'].pop('visual_confirmation_ref')
        self.save()
        self.assert_blocked('requires visual-confirmation file')

    def test_visual_ref_without_policy_still_blocks_proposed_design(self):
        self.files['project.json'].pop('visual_confirmation_policy')
        self.files['visual-confirmation.json']['status'] = 'proposed'
        self.save()
        self.assert_blocked('requires confirmed mockup design')

    def test_mockup_requires_explicit_confirmation_source(self):
        self.files['visual-confirmation.json']['confirmation_source'] = 'unknown'
        self.save()
        self.assert_blocked('confirmed mockup design requires confirmation_source')

    def test_changed_design_cannot_be_approved_by_repreparing_authorization(self):
        self.files['execution-reference.md'] += 'Changed typeface after the visual decision.\n'
        self.save()
        self.assert_blocked('visual confirmation: execution reference changed')

    def test_mockup_requires_target_output_dimensions(self):
        buffer = io.BytesIO()
        Image.new('RGB', (100, 100)).save(buffer, format='PNG')
        self.binary_files['mockup.png'] = buffer.getvalue()
        self.files['visual-confirmation.json']['mockups'][0]['image_digest'] = hashlib.sha256(buffer.getvalue()).hexdigest()
        self.save()
        self.assert_blocked('mockup dimensions must match target output')

    def test_mockup_cannot_reference_an_unavailable_original(self):
        self.files['visual-confirmation.json']['mockups'][0]['source_frame_id'] = 'F001'
        self.save()
        self.assert_blocked('requires an available original keyframe image')

    def test_used_original_keyframe_change_invalidates_visual_confirmation(self):
        self.binary_files['keyframe-visual.png'] += b'changed'
        self.save()
        self.assert_blocked('original keyframe changed since visual confirmation')

    def test_pending_mockup_allows_planning_but_never_rendering(self):
        self.files['timeline.json']['status'] = 'draft'
        self.files['project.json']['render_authorized'] = False
        self.files['visual-confirmation.json'].update(status='proposed', mockups=[])
        self.files['project.json']['execution_reference_asset_refs'] = []
        self.save()
        self.assertEqual(validate(self.root)['status'], 'pass')
        plan = compile_manifest(self.root, planning=True)
        self.assertFalse(plan['render_allowed'])
        with self.assertRaises(ValueError):
            check(self.root, plan)

    def test_music_mode_confirmation_also_requires_sound_form(self):
        self.files['music-direction.json'].pop('sound_form')
        self.save()
        self.assert_blocked('explicit sound_form')

    def test_required_separation_needs_a_fallback(self):
        self.files['music-direction.json']['dialogue_separation'] = 'required'
        self.save()
        self.assert_blocked('separation_fallback')

    def test_add_music_cannot_reference_a_missing_asset(self):
        self.files['music-direction.json'].update(sound_form='add_music', music_asset_ref='missing.wav')
        self.save()
        self.assert_blocked('selected music asset is missing')

    def test_music_led_cannot_skip_music_map(self):
        self.files['music-direction.json']['confirmed_mode'] = 'music_led'
        self.save()
        self.assert_blocked('requires music_map_required=true')

    def test_music_map_complete_label_does_not_replace_analysis(self):
        self.add_music_map()
        self.files['music-map.json'] = {'analysis_status': 'complete'}
        self.save()
        self.assert_blocked('must contain editing anchors')

    def test_music_map_anchors_must_be_inside_music_duration(self):
        self.add_music_map()
        self.files['music-map.json']['beat_positions_ms'] = [10000]
        self.save()
        self.assert_blocked('positions within duration')

    def test_music_map_must_match_selected_asset(self):
        self.add_music_map()
        self.files['music-map.json']['music_asset_ref'] = 'other.wav'
        self.save()
        self.assert_blocked('must reference the selected music asset')

    def test_music_map_duration_is_checked_against_audio_bytes(self):
        self.add_music_map()
        self.files['music-map.json']['duration_ms'] = 12000
        self.save()
        self.assert_blocked('duration must match inspected music asset')

    def test_music_selection_must_fit_actual_asset_duration(self):
        self.add_music_map()
        self.files['music-direction.json']['music_selection']['end_ms'] = 11000
        self.save()
        self.assert_blocked('range must be inside the inspected music asset')

    def test_music_map_requires_AV_mapping(self):
        self.add_music_map()
        self.files['music-map.json']['av_mapping'] = []
        self.save()
        self.assert_blocked('requires explicit AV mapping')

    def test_protected_event_cannot_be_adjusted_to_music(self):
        self.add_music_map()
        self.files['music-map.json']['av_mapping'][0]['relationship'] = 'picture_to_music'
        self.save()
        self.assert_blocked('protected event cannot be adjusted to a music beat')

    def test_changed_music_file_blocks_old_authorization_and_manifest(self):
        self.add_music_map()
        self.save()
        manifest = compile_manifest(self.root)
        path = self.root / 'music.wav'
        path.write_bytes(path.read_bytes() + b'changed')
        self.assert_blocked('selected music asset digest changed')
        with self.assertRaises(ValueError):
            check(self.root, manifest)

    def test_section_mapping_without_beat_grid_is_allowed(self):
        self.add_music_map()
        self.files['music-direction.json']['confirmed_mode'] = 'music_led'
        music_map = self.files['music-map.json']
        music_map.update(tempo_bpm=None, beat_positions_ms=[],
            sections=[{'anchor_id': 'intro', 'start_ms': 0, 'end_ms': 10000, 'label': 'synthetic section'}])
        music_map['av_mapping'][0]['music_ms'] = 0
        self.save()
        self.assertEqual(validate(self.root)['status'], 'pass')
        self.assertTrue(compile_manifest(self.root)['render_allowed'])

    def test_proposed_music_map_can_remain_pending_during_planning(self):
        self.files['music-direction.json'].update(status='proposed', confirmed_mode=None,
            music_map_required=True, music_map_ref='not-yet-made.json')
        self.files['timeline.json']['status'] = 'draft'
        self.files['project.json']['render_authorized'] = False
        self.save()
        self.assertEqual(validate(self.root)['status'], 'pass')
        self.assertFalse(compile_manifest(self.root, planning=True)['render_allowed'])

    def test_added_music_must_be_used_by_final_audio_tracks(self):
        self.add_music_map()
        self.files['music-direction.json']['sound_form'] = 'add_music'
        self.save()
        self.assert_blocked('must appear in final audio_tracks')

    def test_added_music_track_is_bound_to_confirmed_selection(self):
        self.add_music_map()
        self.files['music-direction.json']['sound_form'] = 'add_music'
        self.files['timeline.json']['audio_tracks'].append({
            'track_id': 'MUSIC', 'asset_ref': 'music.wav', 'kind': 'music',
            'source_in_ms': 0, 'source_out_ms': 5000,
            'anchor_event_id': 'E001', 'local_in_frame': 0, 'local_out_frame': 125,
            'gain_db': -12, 'speed': 1, 'fade_in_ms': 0, 'fade_out_ms': 0,
            'narrative_role': 'emotional_music', 'treatment_reason': 'Synthetic background test.'})
        self.save()
        self.assertEqual(validate(self.root)['status'], 'pass')
        self.assertTrue(compile_manifest(self.root)['render_allowed'])
        self.files['music-direction.json']['music_selection']['end_ms'] = 4000
        self.save()
        self.assert_blocked('must stay inside the confirmed music selection')

    def test_partial_section_music_excerpt_remains_valid(self):
        self.add_music_map()
        self.files['music-direction.json']['music_selection'].update(start_ms=1000, end_ms=6000)
        self.files['music-map.json'].update(beat_positions_ms=[],
            sections=[{'anchor_id': 'section-1', 'start_ms': 0, 'end_ms': 10000, 'label': 'synthetic section'}])
        self.files['music-map.json']['av_mapping'][0]['music_ms'] = 1000
        self.save()
        self.assertEqual(validate(self.root)['status'], 'pass')

    def test_same_source_mix_requires_no_added_music_or_map(self):
        self.assertEqual(validate(self.root)['status'], 'pass')
        self.assertTrue(compile_manifest(self.root)['render_allowed'])

    def available_keyframe(self):
        self.files['keyframe-references.json'][0].update(
            status='available', image_ref='keyframe.png')
        self.save()
        # Tiny synthetic PNG fixture, not a claimed frame from a real source.
        (self.root / 'keyframe.png').write_bytes(base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wl2hEQAAAAASUVORK5CYII='))

    def alternate_unit(self):
        source = self.files['sources.json'][0].copy()
        source['source_id'] = 'SRC002'
        self.files['sources.json'].append(source)
        self.files['units.jsonl'].append({
            'unit_id': 'U002', 'source_id': 'SRC002', 'scene_id': 'S002',
            'start_ms': 0, 'end_ms': 8000, 'utterance_ids': [], 'protected_ranges': []})
        self.files['scenes.jsonl'].append({
            'scene_id': 'S002', 'source_ranges': [
                {'source_id': 'SRC002', 'start_ms': 0, 'end_ms': 8000}],
            'facts': ['synthetic alternate scene'], 'unknowns': []})

    def test_available_keyframe_matches_unit_and_existing_frame(self):
        self.available_keyframe()
        self.assertEqual(validate(self.root)['status'], 'pass')
        manifest = compile_manifest(self.root)
        self.assertEqual(check(self.root, manifest)['status'], 'pass')

    def test_nonexistent_keyframe_unit_is_blocked(self):
        self.available_keyframe()
        self.files['keyframe-references.json'][0]['source_segment'] = 'MISSING_UNIT'
        self.save()
        self.assert_blocked('unknown source_segment unit')

    def test_unavailable_keyframe_cannot_reference_a_nonexistent_unit(self):
        self.files['keyframe-references.json'][0]['source_segment'] = 'MISSING_UNIT'
        self.save()
        self.assert_blocked('unknown source_segment unit')

    def test_keyframe_unit_source_must_match(self):
        self.alternate_unit()
        self.files['keyframe-references.json'][0]['source_segment'] = 'U002'
        self.available_keyframe()
        self.assert_blocked('source_segment source mismatch')

    def test_keyframe_time_must_match_reused_frame_id(self):
        self.available_keyframe()
        self.files['keyframe-references.json'][0]['timestamp_ms'] = 1100
        self.save()
        self.assert_blocked('timestamp_ms must match existing frame')

    def test_unavailable_keyframe_keeps_known_frame_time_consistent(self):
        self.files['keyframe-references.json'][0]['timestamp_ms'] = 1100
        self.save()
        self.assert_blocked('timestamp_ms must match existing frame')

    def test_keyframe_source_must_match_reused_frame_id(self):
        self.alternate_unit()
        self.files['keyframe-references.json'][0].update(
            source_segment='U002', source_id='SRC002')
        self.available_keyframe()
        self.assert_blocked('source_id must match existing frame')

    def test_keyframe_time_must_be_inside_its_unit(self):
        self.available_keyframe()
        self.files['keyframe-references.json'][0].update(
            frame_id='NEW_FRAME', timestamp_ms=8000)
        self.save()
        self.assert_blocked('timestamp_ms is outside source_segment')

    def test_new_keyframe_id_inside_known_unit_remains_allowed(self):
        self.available_keyframe()
        self.files['keyframe-references.json'][0].update(
            frame_id='NEW_FRAME', timestamp_ms=2000)
        self.save()
        self.assertEqual(validate(self.root)['status'], 'pass')

    def test_overwritten_keyframe_image_invalidates_old_render_entry(self):
        self.available_keyframe()
        manifest = compile_manifest(self.root)
        image = self.root / 'keyframe.png'
        image.write_bytes(image.read_bytes() + b'changed-synthetic-image-bytes')
        self.assertEqual(validate(self.root)['status'], 'pass')
        with self.assertRaisesRegex(ValueError, 'inputs changed'):
            check(self.root, manifest)
        self.assertNotEqual(compile_manifest(self.root)['input_digest'], manifest['input_digest'])

    def test_unavailable_keyframe_requires_exception_file(self):
        (self.root / 'structure-exceptions.jsonl').unlink()
        self.assert_blocked('unavailable requires a matching exception declaration')

    def test_unavailable_keyframe_exception_must_match_record(self):
        self.files['structure-exceptions.jsonl'][0]['record_id'] = 'OTHER_FRAME'
        self.save()
        self.assert_blocked('unavailable requires a matching exception declaration')

    def test_unavailable_keyframe_exception_must_match_field(self):
        self.files['structure-exceptions.jsonl'][0]['field'] = 'narrative_role'
        self.save()
        self.assert_blocked('unavailable requires a matching exception declaration')

    def test_unavailable_keyframe_exception_must_match_status(self):
        self.files['structure-exceptions.jsonl'][0]['status'] = 'partial'
        self.save()
        self.assert_blocked('unavailable requires a matching exception declaration')

    def test_unavailable_keyframe_accepts_explicit_artifact_exception(self):
        self.files['structure-exceptions.jsonl'][0].update(record_id=None, field='*')
        self.save()
        self.assertEqual(validate(self.root)['status'], 'pass')


if __name__ == '__main__':
    unittest.main()
