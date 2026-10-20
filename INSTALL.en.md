# Install and upgrade · v1.3.1

Long Video Remix is an **AI video editing Agent Skill for Claude Code and Codex**, covering long video to shorts, video highlights, Visual Methods, Blender motion composition, FFmpeg rendering, and QA.

Schema 1.9 and the v1.3.0 Blender motion-proof checkpoints remain unchanged. v1.3.1 adds a Direct 2 Style System / Visual Router / method-and-fallback knowledge layer without adding a stage, gate, schema, or QA layer. Read [visual production](references/visual-production.md); install Blender separately for native renders, and FFmpeg/ffprobe for video validation and final return. No bundled Blender/MCP service is implicitly installed. Adopt on an existing project with `python scripts/visual_pipeline.py init PROJECT`; existing evidence and decisions are preserved, never auto-approved. Actual platform validation is listed in [release QA](docs/qa/v1.3.1-QA.md).


Keep the complete `long-video-remix/` directory together: `SKILL.md`, `references/`, `assets/`, `scripts/`, `tests/`, and `agents/`. Copying `SKILL.md` alone drops the contracts and validation tools.

## Install

```sh
# Claude Code
mkdir -p ~/.claude/skills
git clone https://github.com/hazelliuliu1823-cloud/long-video-remix.git ~/.claude/skills/long-video-remix

# Codex
mkdir -p ~/.agents/skills
git clone https://github.com/hazelliuliu1823-cloud/long-video-remix.git ~/.agents/skills/long-video-remix
```

You may also place the extracted `long-video-remix` folder under `~/.claude/skills/` or `~/.agents/skills/`. Keep source media and project data outside the skill directory.

After the `v1.3.1` tag is published, a pinned install can use:

```sh
git clone --branch v1.3.1 --depth 1 https://github.com/hazelliuliu1823-cloud/long-video-remix.git TARGET
```

## Runtime

- Validation, authorization, manifest compilation, and regression tests: Python 3.9+ standard library.
- `extract_frames.py` and export auditing: FFmpeg / ffprobe; contact-sheet generation additionally uses Pillow.
- Models, video MCPs, and renderers are discovered from the current environment and recorded in `capability-map.json`; the package does not download large models or media.
- The current v1.3.1 regression environment is Python 3.13.5 + FFmpeg 7.1.5 + Pillow 12.3.0. It discovers 265 tests: 263 pass, 2 are conditionally skipped because `BLENDER_EXECUTABLE` is not configured in this run, and 0 fail. v1.3.0 QA retains the earlier actual Blender/FFmpeg synthetic-render evidence; v1.3.1 does not present that historical evidence as rerun. Integration tests skip when their FFmpeg / Pillow / Blender dependency is unavailable.

## Verify the installation

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_project.py examples/synthetic-ready
python3 scripts/compile_render_manifest.py examples/synthetic-ready
python3 scripts/check_render_authorization.py examples/synthetic-ready examples/synthetic-ready/render-manifest.json
```

The bundled example is synthetic. It demonstrates the data and Visual Gate path, not real-video understanding or aesthetic quality.

## Upgrade from v1.2.3

- No new creative stage, formal CSV header, or authorization schema is added. For project schema 1.8, Direct 2 now stores planned in/out, selected boundary, the then-current safe windows, and allowed adjustments in a source event `d2_selection_snapshot`; Execute Step 0 may calibrate only inside that snapshot. Exceeding it, widening safe windows, or switching the boundary stops for confirmation.
- Schema 1.7 regains the v1.2.2 boundary strictness. Only schema 1.8+ may defer exact unselected-candidate boundary precision.
- A Visual Proof is no longer satisfied by any available capability: the capability must have `actual_tool + entrypoint` and an `output_mapping` that resolves to the current `visual_proof_ref`.
- `project.schema_version` accepts dotted numeric versions such as `1.8` only; values such as `v1.8` or `1.8-rc1` are errors instead of legacy fallbacks.
- Checksum regression verifies only files listed in `SHA256SUMS`, so `.git/`, `.DS_Store`, and other local clone metadata do not break installation verification. `.gitattributes` pins repository text to LF to reduce Windows checksum drift.

## Upgrade from v1.2.2

- New projects use project schema 1.8; formal CSV headers are unchanged.
- Detail candidates may keep selection-ready `partial` edit boundaries, with exact audio/action tails deferred until the clip is actually selected.
- Direct 2 hands off planned ranges + boundary refs. Execute Step 0 then reopens only selected ranges + handles and promotes adopted boundaries to `supported`; schema 1.8+ requires that before `ready_for_render`.
- Full-interval ASR is not a Detail completion requirement. Prefer reliable subtitles plus signals / waveform and use targeted ASR only where needed.
- Prepare / confirm execution authorization after Step 0 against the final adopted source ranges. Schema 1.7 projects retain v1.2.2 compatibility behavior.

## Upgrade from v1.2.1 / v1.2.0

The creative workflow remains `Broad Structure → Direct 1 → Detail Structure → Direct 2 → Execute`. Formal CSV headers are unchanged. Project schema 1.7 is introduced only to distinguish new projects, where the Visual Gate is mandatory, from schema 1.6 legacy projects. No current-state, visual-style, toolchain, or music-gate file is added.

- **Scope Lock:** keep the four lines inside existing Direct / handoff documents: current stage, editable, locked, rejected.
- **Detail STOP:** stop dense review once the target question, minimum complete interaction / action unit, Edit Boundary, and relevant counterevidence are closed.
- **Visual Gate:** schema 1.7 projects must use `execution_package_policy=plan_and_reference` and contain `visual_gate_status`, `visual_mockup_ref`, and `visual_proof_ref`. Aesthetic Mockup may be confirmed in one model or session; Executable Proof may be completed later elsewhere, but it must use a tool and entrypoint that final Execute can actually call.
- **Toolchain continuity:** copy `assets/capability-map-template.json` to `capability-map.json` and record the real `actual_tool` and `entrypoint`. `proof_confirmed` requires at least one available capability with both fields.
- **Proof identity:** the selected mockup and executable proof must be separate files with different content, and both must be included in `execution_reference_asset_refs`.

Schema 1.6 legacy projects keep the previous compatibility behavior. Migrating them to 1.7 does not require re-running Broad or Detail; add the Visual Gate fields, capability map, mockup / proof assets, and refresh Direct 2 authorization. The current `examples/synthetic-ready` project uses schema 1.8 and includes the same Visual Gate path plus the selected-range verification state introduced in v1.2.3 and hardened in v1.2.4.

## Older projects

Existing source evidence, stable question IDs, Detail observations, edit boundaries, and confirmed narrative decisions remain reusable. When an older project is moved onto the current execution-package format, preserve its evidence and only add the missing handoff / reference / authorization records required by the current validator. See `references/execution-package.md`, `references/execution-integrity.md`, and `references/data-contracts.md` for the full contracts.

## Source-material rights

Only process and publish media you are authorized to use. The skill's validation and rendering checks do not grant rights to third-party footage, music, fonts, or other assets.
