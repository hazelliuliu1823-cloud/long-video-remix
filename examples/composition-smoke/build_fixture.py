#!/usr/bin/env python3
"""Generate synthetic media and pending production records. Never approve gates."""
import argparse
import array
import json
import math
from pathlib import Path
import shutil
import sys
import wave

PACKAGE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE / 'scripts'))
import visual_pipeline as vp


def build(root):
    vp.require(not root.exists(), 'Choose a new fixture directory; existing work is preserved')
    shutil.copytree(PACKAGE / 'examples/synthetic-ready', root)
    from PIL import Image, ImageDraw
    media = root / 'media'
    media.mkdir()
    for name, color, direction in [('a', (32, 58, 78), 1), ('b', (64, 43, 54), -1)]:
        image = Image.new('RGB', (320, 180), color)
        draw = ImageDraw.Draw(image)
        draw.rectangle((14, 14, 305, 165), outline=(195, 200, 205), width=2)
        draw.ellipse((72, 54, 112, 94), fill=(210, 208, 200))
        draw.ellipse((205, 54, 245, 94), fill=(210, 208, 200))
        draw.line((94, 74, 225, 74), fill=(152, 179, 190), width=2)
        draw.text((24, 140), 'SYNTHETIC ENGINEERING TEST ' + name.upper(), fill=(225, 225, 225))
        image.save(media / (name + '.png'))
    samples = array.array('h')
    for index in range(5 * 48000):
        value = round(1600 * math.sin(index * 2 * math.pi * 220 / 48000))
        samples.extend((value, value))
    with wave.open(str(media / 'audio.wav'), 'wb') as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(48000)
        handle.writeframes(samples.tobytes())
    project = vp.read(root / 'project.json')
    project['current_stage'] = 'D2'
    project['render_authorized'] = False
    project['execution_plan_status'] = 'not_provided'
    vp.write(root / 'project.json', project)
    timeline = vp.read(root / 'timeline.json')
    timeline['status'] = 'draft'
    vp.write(root / 'timeline.json', timeline)
    project = vp.initialize(root)
    project['output'] = {'width': 320, 'height': 180, 'fps_num': 25, 'fps_den': 1}
    project['workflow_control']['audio_choice'] = {'mode': 'no_music', 'description': 'Synthetic test tone; no music or dialogue claim', 'ref': 'demo-spec.md#Audio'}
    project['workflow_control']['visual_spec_refs'] = ['demo-spec.md#Visual']
    vp.write(root / 'project.json', project)
    (root / 'demo-spec.md').write_text('# Audio\n\nSynthetic stereo test tone only.\n\n# Visual\n\nTwo generated panels; group push and a deliberate cut. Engineering test only.\n', encoding='utf-8')
    vp.write(root / 'visual-methods.json', {'schema_version': '1.0', 'project_id': project['project_id'], 'methods': [{
        'method_id': 'PM001', 'library_refs': ['M13'], 'fallback_refs': ['F09'],
        'event_ids': ['E001'], 'source_evidence_refs': ['DO001'],
        'narrative_role': 'Synthetic engineering example; no real narrative assertion',
        'visual_focus': 'The two circles and their common relation remain visible',
        'source_conditions': 'Generated 320x180 panels with explicit safe margins',
        'original_frame_assessment': 'Use a restrained group push to test saved motion and end-state continuity',
        'selected_treatment': 'Group push, hold the achieved pose, then a declared hard cut to panel B',
        'selection_reason': 'Tests shared motion, absence of reset, and coverage of both sides of a cut',
        'alternatives_considered': [], 'parameters': {'scale_start': 1, 'scale_end': 1.08, 'motion_end_frame': 60, 'cut_frame': 75},
        'failure_modes': ['End pose resets before the cut', 'Foreground and image move independently'],
        'demo_checks': ['Actual frames 60..74 hold the achieved pose', 'Both sides of frame 75 are visible'],
        'composition_required': True}]})
    vp.write(root / 'composition-plan.json', {'schema_version': '1.0', 'project_id': project['project_id'],
        'output': project['output'], 'proof_composition_id': 'C01', 'compositions': [{
            'composition_id': 'C01', 'backend': 'blender', 'mode': 'layers', 'method_ids': ['PM001'],
            'event_ids': ['E001'], 'anchor_event_id': 'E001', 'local_start_frame': 0, 'frame_count': 125,
            'groups': {'push': {'transform': {}, 'keyframes': [{'frame': 0, 'values': {'scale': 1}},
                        {'frame': 60, 'values': {'scale': 1.08}, 'easing': 'smoothstep'}]}},
            'layers': [
                {'layer_id': 'panel-a', 'kind': 'image', 'asset_ref': 'media/a.png', 'start_frame': 0, 'end_frame': 75, 'parent': 'push', 'fit': 'cover'},
                {'layer_id': 'panel-b', 'kind': 'image', 'asset_ref': 'media/b.png', 'start_frame': 75, 'end_frame': 125, 'fit': 'cover'}],
            'joins': [{'frame': 75, 'before_frames': 25, 'after_frames': 25,
                       'from_event_id': 'E001', 'to_event_id': 'E001', 'cut_intent': 'A declared internal panel cut in one synthetic event',
                       'outgoing_state': 'Hold the 1.08 scale; no reset', 'incoming_state': 'Stable full panel B',
                       'motion_handoff': 'End the push before the deliberate cut; no automatic crossfade'}],
            'preview_audio_ref': 'media/audio.wav', 'silent_demo': False,
            'scene_ref': 'compositions/C01/v1.blend', 'video_ref': 'compositions/C01/v1-visual.mp4',
            'demo_ref': 'compositions/C01/v1-demo.mp4', 'proof_ref': 'compositions/C01/v1-proof.png',
            'receipt_ref': 'compositions/C01/v1-render.json', 'readback_ref': 'compositions/C01/v1-readback.json',
            'review_ref': 'compositions/C01/v1-review.json'}]})
    vp.write(root / 'delivery-spec.json', {'schema_version': '1.0', 'project_id': project['project_id'],
        'base_video_ref': 'render/clean-video.mp4', 'mixed_audio_ref': 'media/audio.wav',
        'subtitles_ref': None, 'font_refs': [], 'crf': 18, 'output_ref': 'render/final.mp4'})
    vp.require(project['workflow_control']['confirmations'] == {}, 'Fixture must not contain approval records')
    return {'project': str(root.resolve()), 'status': 'pending_decisions', 'render_authorized': False,
            'scope': 'Synthetic engineering input, not real-media or aesthetic acceptance'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.output.resolve()), ensure_ascii=False, indent=2))
