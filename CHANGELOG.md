# Changelog

## v1.3.1 · 2026-10-20 — Visual Methods 方案生成 / 兜底与轻量交互

- 以 v1.3.0 为主干，**完整保留 Blender 工程、静态 Proof、连续 Dynamic Demo、FFmpeg 回接和最终播放 QA**；schema 仍为 1.9，不改授权与 Composition 契约。
- 集成 Visual Methods 1.5.1 的 Style System、Visual Router、M01–M14 完整方法库、F01–F09 fallback，以及研究 / 资源说明。采用“瘦加载，不瘦知识”：默认读 Router，命中后读取完整方法。
- Visual Methods 正式承担 Direct 2 的方案生成 / 兜底：已有想法时校正深化；只有抽象形容词、常见默认处理、真实画面无法落地或用户要求更强视觉时，主动提出可制作候选、推荐理由、工具可执行性和失败信号。
- 不新增阶段、Gate 或独立 QA；Visual Methods 的检查点映射到现有 Demo Review 与最终 QA。Broad 不选方法，Direct 1 只定语气，Detail 提供真实画面条件，Direct 2 才正式选择。
- 新模板将项目实际方法 ID 改为 `PM001...`，知识库 `M01–M14` / `F01–F09` 通过可选 `library_refs` / `fallback_refs` 引用，避免 ID 冲突；旧项目 method ID 保持兼容。
- 默认用户交互收敛成两个 confirmation bundle：D2 Design Lock 与 Production Proof Lock。内部 Gate 仍独立保存 digest / stale 状态，确认束不扩大用户授权。
- Public packaging refresh: README 首屏与双语 Use Cases 强化 `AI video editing`、`long video to shorts`、`video highlights`、`Blender`、`FFmpeg` 等用户检索入口；Release / install / Agent metadata 同步当前 v1.3.1 能力定位，不改变工作流或 schema。

## v1.3.0 · 2026-10-18 — 制作方法、Blender 工程与动态确认

- 基于 v1.2.4 完整底稿，承接 v1.2.5 续接关口；A–G、两次 Direct、正式 CSV 与原授权 schema 保持不变。
- 新项目 schema 1.9：叙事作用/视觉重点/处理依据/参数与失败情形形成可确认方法。
- 新增固定 2D Blender 适配器（图层、父子组、曲线与末尾状态）和原生 .blend 工程路径，实际渲染后交连续 demo、readback、receipt、静态 proof 与待填 review。
- method / composition 关口接入构建、授权草稿、正式编译与 FFmpeg 回接；参数、源范围、工程或资源变化会使旧验证失效。
- 复杂窗口回接既有 FFmpeg clean-video / mix，保留原 QA，并要求 CompositionCompliance、MotionContinuity、DeliveryTechnical。输出成功不自动通过审美、用户确认或最终 QA。
- 两种完整源码包使用同一核心；实际验证与限制见 `docs/qa/v1.3.0-QA.md`。

## v1.2.5 · 2026-10-18 — 阶段内关口与 Chat 续接

- 大阶段、两次 Direct、正式 CSV 和 project schema 1.8 保持不变。新增统一 workflow_control 状态，存入原 project.json。
- 同一项目续接先恢复有效/待确认/失效关口；声音策略、Mockup、Proof、计划与证据绑定，变动只重开受影响记录。
- 授权草稿与 ready_for_render 验证接入强制检查；跨大块推进要通过对应出口；partial handoff 保留全部未过关口。
- 新模板默认启用；旧项目由 init 补控制记录，不重扫、不自动确认。QA 绑定实际成片指纹。
- Chat 外层提供项目说明与完整文字参考作为持续上下文；不宣称插件文件能够强制宿主每轮加载。



## v1.2.4 — Gate & Compatibility Hardening · 2026-10-17

- Fixed checksum regression for real Git installs: the test now verifies the files declared by `SHA256SUMS` instead of treating `.git/` or local OS metadata as packaged files; added `.gitattributes` with LF text normalization.
- Restored schema 1.7 boundary strictness. The deferred partial-boundary precision introduced in v1.2.3 applies only to schema 1.8+ projects.
- Unified strict project schema parsing in one shared helper. Malformed values such as `v1.8` and `1.8-rc1` are errors rather than silent legacy fallbacks.
- Corrected the `capability-map.json` contract to the actual `{schema_version, capabilities:[...]}` object format. Visual Proof now requires an available capability whose `output_mapping` resolves to the declared `visual_proof_ref`, not merely any tool with an entrypoint.
- Added a compact `d2_selection_snapshot` on schema 1.8 source events. It records the Direct 2 planned range, selected boundary, safe windows, and allowed trim / handle adjustments; Execute Step 0 cannot widen that envelope or switch the boundary without returning for confirmation.
- `prepare_execution_authorization.py` carries the snapshot's allowed adjustments into the draft authorization; the existing event spec / asset fingerprints continue to lock the final confirmed state.


## v1.2.3 — Selected Range Verification · 2026-10-17

- Moved final A/V boundary precision out of every Detail candidate and into **Execute Step 0**, which reopens only Direct 2 selected ranges + handles.
- Detail is now explicitly subtitle + waveform / signals first. Full-interval ASR is not a completion condition; targeted ASR is used only for decisive wording / speaker ambiguity or final subtitle needs.
- `edit-boundaries.csv` keeps the same header. `partial` now supports selection-ready conservative boundaries with unknown exact audio/action tails; `supported` means the applicable continuity boundary has been verified.
- New projects use project schema 1.8. `ready_for_render` requires each selected source event's boundary to be `supported`, while unselected partial candidates may remain untouched. Schema 1.7 keeps the v1.2.2 ready behavior.
- Direct 2 may run in another model/session and hand off planned ranges + boundary refs + allowed calibration. Execute Step 0 may calibrate boundaries but may not change narrative selection; semantic conflicts return to Direct 2. Final machine authorization is prepared / confirmed after Step 0 against the actual adopted ranges.
- No Audio Gate, Audio Closure file, new creative stage, timeline schema, authorization schema, or formal CSV header was added. Visual Gate and Toolchain Continuity are unchanged.

## v1.2.2 — Release Hardening · 2026-10-17

- Bumped `project.json` to schema 1.7 for new projects so the three-field Visual Gate cannot be bypassed by omission; schema 1.6 projects retain compatibility behavior.
- `proof_confirmed` now requires distinct mockup / proof content plus `capability-map.json` with at least one available `actual_tool + entrypoint`; all three are authorization-bound reference assets, so toolchain-entry changes invalidate old confirmation.
- Upgraded `examples/synthetic-ready` to exercise the current Detail handoff, keyframe reference, execution reference, capability map, mockup, executable proof, and authorization path.
- Added `assets/capability-map-template.json`, an English install guide, Direct 2 / Render+QA prompt examples, canonical stage naming, and corrected Execute-vs-Detail responsibilities in both READMEs.
- Added a checksum regression test so edits cannot silently leave a stale repository `SHA256SUMS`.

## v1.2.1 — Lean Scope & Visual Reproducibility Gate · 2026-10-17

- Added a minimum-sufficient Detail STOP rule without adding tables or stages.
- Replaced the heavier state-file idea with a four-line Scope Lock carried inside existing Direct / handoff documents.
- Split visual confirmation into Aesthetic Mockup and Executable Proof Frame. Proof may be completed in another model or session, but must use the same real execution toolchain available to final Execute; the existing `capability-map.json` carries that mapping.
- Added only three project fields (`visual_gate_status`, `visual_mockup_ref`, `visual_proof_ref`). No current-state, visual-style, music-gate file, formal CSV, or schema-version change. Legacy projects without these fields retain v1.2.0 warning-only behavior.

## v1.2.0 — Keyframe Mockup Handoff · 2026-10-08

- Detail delivers individual original keyframes with its existing index and handoff. Direct 2 uses real keyframes to produce full-canvas mockups and binds them to typography, layout parameters, required resources and a reusable layout source or rendering method.
- Execute reuses the same design and resources; mockups lock the style, and QA checks style match between output and mockup without frame-exact or pixel-exact requirements. One or two representative samples normally establish the film's style; include special layouts only when used. Missing images or rendering capability are recorded as pending, without substituting generated evidence or treating parameters as a completed mockup.
- Updated existing instructions, templates and bilingual release documentation; no new package files, creative stages, scripts, formal CSV headers or schema versions. SKILL.md remains 23,447 of 23,842 bytes.
- Review round (still v1.2.0): acceptance wording changed from pixel-level reproduction to style match; mockup rules consolidated in `references/execution-package.md` (templates keep fields; the handoff template keeps a short self-contained summary); font-licence risk noted for commercial use; `validate_project.py` warns, without blocking, when a ready_for_render package declares no mockup / reference image; added `docs/qa/v1.2.0-QA.*`. 2 tests added (192 total) under Python 3.12.3 + FFmpeg 6.1.1 + Pillow; the new visual handoff otherwise has no automated checks.

## v1.1.0 — Lean Detail Rebuild on v1.0.7 · 2026-10-07

Rebuilt on v1.0.7. The v1.0.8–v1.0.10 development line is not carried forward; its lessons are kept in a smaller form.

- Added `scripts/extract_frames.py` for local identity-mapped sources (Broad sampling, Detail reading, edit-point strips). Every label is measured, never `start + index / fps`; other environments use validated MCP adapters and retain existing time mappings. `signals` reports local visual change, hard-cut candidates and sound / silence segments. Cleanup requires a dedicated ownership record, touches tracked outputs only and protects project/source ancestors.
- Added `references/detail-evidence.md`, read only in stage E: full coverage with content-driven density (context 0.5 fps, static core 1 fps, change / candidate / question windows 4 fps), each moment read once, mandatory full-resolution frames at decisive moments, no thumbnail-only verdicts on fine actions, bracket-then-strip edit points, single-context dense reading.
- Added `scripts/detail_gates.py`: Detail files are linted as soon as they exist; completed Detail requires stable target question IDs answered by observations; contradicted / unresolved questions are closed in one place, the handoff Question Closure Ledger; at ready_for_render a selected node cannot carry an unresolved question, and a contradicted one needs a human `confirmed_by`.
- Added `assets/benchmark-template.md` (reads per density, repeated reads, edit-point rework, Detail writing time, full re-read audit).
- Capped instruction size: `tests/test_size_budget.py` keeps SKILL.md within the v1.0.7 size (now 23,445 of 23,842 bytes) and `references/workflow.md` within its v1.0.7 size; field lists in SKILL.md now point to data-contracts, which the validator already enforces.
- The synthetic example now carries its Q001 question row; its authorization evidence digest and render manifest were refreshed accordingly. Formal CSV headers are unchanged.
- Review repair is limited to directory cleanup, question closure and extraction adapters: unique question/ledger IDs and source/interval/node consistency are checked against actual evidence links. Early Detail numeric lint remains unchanged; no new package files or schemas.
- Second review round: the Question Closure Ledger is recognized under any heading that contains "Question Closure Ledger" or "问题闭环" (a Chinese note is fine), with an explicit hint when no such section exists; INSTALL / RELEASE_NOTES now list all four project migrations (stable question IDs, observation-interval node consistency, question-interval consistency, the closure ledger); MCP frame adapters must prove measured timestamps in a short probe and record `timestamp_method`, and `computed` adapters are not used for Detail facts or edit points. 4 tests added (190 total), passing under Python 3.12.3 + FFmpeg 6.1.1 + Pillow; the 3 heading tests fail on the previous build.
- 33 new tests versus v1.0.7 (186 total, including 9 review-repair tests) passed under Python 3.12.14 + FFmpeg 6.1.1 + Pillow. Frame-timing tests decode picture content; with default fps rounding and computed labels they fail. No real long-video benchmark has been run yet.

## v1.0.7 — Prompt Examples & Bilingual Guide · 2026-10-03

- Included four matching Chinese and English README prompt examples with their expected deliverables: start Broad Structure, propose directions from Broad, locate Detail intervals for a confirmed direction, and complete Detail with a self-contained handoff.
- Kept the existing first-screen positioning, workflow illustration, core-value table, folded method, and content-performance example.
- Updated the release version, installation and update guidance, release notes, and package checksums. Existing v1.0.6 project data and confirmed plans remain reusable.
- Preserved all engineering scripts, tests, templates, contracts, examples, agent metadata, and historical QA records byte for byte.
- Re-ran all 153 regression tests under Python 3.12.14 and the synthetic example's validation, compilation, and render-authorization checks; all passed. Real-video analysis and playback were not re-tested for this documentation release.

## v1.0.6 — Structure Exceptions & Execution Package · 2026-10-01

- Kept existing stages, two Direct decisions and locked Structure schemas; added explicit unavailable / uncertain / partial declarations with reason, impact and downstream handling so feasible Structure / draft / handoff work continues without fabricated facts.
- Added a small real-source Keyframe Reference deliverable inside Detail, with extraction exceptions and source-time traceability.
- Added a self-contained Detail handoff that carries narrative context, selected clips, evidence / protection, images and the downstream complete Execution Package requirements across model boundaries.
- Defined Direct 2 output as Execution Plan + Production Reference, with actionable text / audio / transition specifications, assets, constraints and QA; added reusable handoff / reference templates.
- Replaced per-visual matching with Reference Application Rules: one or two representative style samples define whole-video design rules; no per-shot / subtitle mapping.
- Made Execute consume the full confirmed package and added Reference Compliance to existing QA. Declared reference document / asset changes invalidate old confirmation and render entry; undeclared legacy project behavior remains unchanged.
- Preserved all original CSV templates, historical examples / tests, timeline math, rendering algorithms, caches, dialogue protection and authorization requirements.

### 2026-10-02 — Keyframe integrity fixes

- Checked keyframe source units and source times against unit ranges and existing frame records.
- Included actual keyframe image bytes in input fingerprints so replacing an image invalidates an old render entry.
- Required unavailable keyframes to match a synchronized exception declaration.
- Added 15 regression cases; all 153 tests passed in the engineering validation.

### 2026-10-02 — Bilingual documentation and release preparation

- Added a complete English README with reciprocal language links; Chinese remains the default.
- Shortened the introduction while retaining lower-cost reuse, rich structure, human Direct decisions, reliable Execute, the folded method, and the content-performance example.
- Corrected both file trees, archived historical QA under docs/qa, and updated affected links and SHA256SUMS.
- Added English skill-description keywords, concrete local installation commands, and a source-material rights statement; aligned copyright attribution with hazelliuliu1823-cloud.
- Kept scripts, tests, templates, contracts, agent metadata, and examples unchanged.

## v1.0.5 — Independent Source Audio Dialogue · 2026-10-01

- Fixed F4: derive and validate utterances independently for every adopted source audio track, including card-only speech, unassociated extra tracks and audio-only sources. Full current utterance evidence and audio verification are required before preservation decisions.
- Included audio-only utterances and their dedicated reviews in adopted_evidence_digest. Changes invalidate unchanged confirmation; recompilation must still reject stale evidence.
- Preserved source-event synchronization and existing event-level exceptions. Independent speech permits asynchronous output placement, compatible continuation across cards and valid track-level audio_required_range exceptions; explicit policy changes require a track-level reason.
- Added independent speech regression cases and v1.0.4 migration guidance. Retained all formal CSV templates, original core scripts, two Direct stages, layered caches, render audit and previously declared capability boundaries.

## v1.0.4 — Dialogue Selection & Full Audio Review Coverage · 2026-10-01

- Fixed F1: validate explicitly adopted utterances and known same-source speech intersecting actual video / associated audio selections before checking self-declared protection ranges. Missing, stale or unverified adopted speech cannot be filtered out by an underdeclared audio boundary.
- Fixed F2: dialogue preservation is triggered by adopted speech / speech metadata independently of continuity_type. Scene or action labels cannot allow muted, replaced or misaligned preserved dialogue. Explicit policy changes require a confirmed event-level reason.
- Fixed F3: every source audio track requires independent current audio review_refs covering its complete source range, including J/L-cut extensions. Track-only reviews enter the adopted evidence digest; creative exceptions do not grant review coverage.
- Added explicit adopted_utterance_refs to ready source events, migration instructions, positive and negative regression cases, and a refreshed synthetic-ready example.
- Preserved the six formal Structure CSV templates, two Direct stages, timeline math, layered caches and render audit. Broad coverage, sampling / semantic proof, Deep protection transfer and non-dialogue audio closure remain explicitly bounded.

## v1.0.3 — Structured Representation & Execution Integrity · 2026-10-01

- Added current-source / time-mapping bindings for adopted observations, boundaries, reviews, unit verification, utterances, video events and source audio tracks; stale evidence blocks ready execution.
- Added a machine-readable Direct 2 execution authorization, with selected events / units / boundaries, exact sequence, adopted evidence snapshot, track / transition recipes and explicit permitted adjustments. Decision or evidence changes invalidate its fingerprints.
- Extended existing Edit Boundary protection to source-audio coverage, duration, source/output synchronization and fades; explicit supported J/L-cut and creative tail-cut exceptions remain possible.
- Enforced source_scope, usable_ranges, optional allowed_scope and typed source-range constraints against actual video and audio adoption.
- Required precise override targets, violated rules, current successful review coverage and confirmed creative decisions; placeholder and unrelated overlap/boundary reviews no longer release execution.
- Default compilation now rejects non-ready or unauthorized drafts; --planning carries render_allowed=false. Added a current-input / manifest-integrity guard for renderer adapters.
- Added output fps to mix_audio cache identity while retaining the existing layered cache design, cumulative timeline math and render-audit script.
- Reworked the README first screen around lower repeated multimodal-understanding cost, reusable rich structure and human creative direction. Preserved complete technical content and added installation, migration, release, executable regression and synthetic-ready files.
- Preserved the six formal Structure tables, two Direct stages and original render QA. This release does not claim automatic proof of all coverage, sampling or semantic judgments.

## v1.0.2 — Compact multimodal structure for lower-context reuse

- Added a hard **Edit Boundary / Continuity Layer** between Detailed Structure and Direct 2: `edit-boundaries.csv` records real audio tails, action/reaction settle points, preferred in/out, safe windows, must-keep ranges, handles and cut risk.
- `ready_for_render` now requires every selected source event to reference an explicit edit boundary; default cuts must land inside the safe windows and preserve must-keep ranges. Deliberate boundary violations require an explicit override reason and review references.
- Added boundary-aware validation / compilation so subtitle or ASR endpoints cannot silently become cut points, while preserving all existing Structure, two-Direct, evidence, timeline, cache and render-QA behavior.
- Fixed final-layer cache identity for generated card text: changing `card_text` or card text-render parameters now invalidates only the final composited cache, while clean-video and audio caches remain reusable when otherwise safe.
- Fixed validator preflight when Directed Deep / Detail is incomplete: Deep indexes are initialized safely and evidence-linkage checks are skipped until the stage is complete, so ready-state violations return structured validation/compiler errors instead of crashing.
- Refined Execute evidence linkage from coarse `unit_id` aggregation to explicit event-level `deep_observation_refs`; adopted observations are now checked for source identity, source-time coverage, and current evidence status, while unrelated observations in the same unit do not block execution.
- Added dependency-aware cache reuse reporting: unknown audio source / asset versions disable `mix_audio` and `final` reuse without unnecessarily disabling known video-layer caches; `cache_reusable` remains the backward-compatible final aggregate flag.
- Synced README responsibility wording so evidence verification stays in Directed Deep / Detail Structure, and added `timeline_math.py` to the repository tree.

- Clarified the canonical workflow without changing the confirmed Structure / Execute capabilities: Broad Structure now explicitly exits as a **formal textual Structured Observation Layer** (observation tables + scene/segment roll-ups) before Content Map; Direct is explicitly two-pass — first Narrative Direction, then post-Detail Editorial Execution Plan.
- Added `assets/narrative-direction-template.md` and `assets/execution-plan-template.md`; legacy `editorial-plan-template.md` remains for compatibility. Execute is not allowed to skip the second Director decision and invent the final storytelling plan from evidence alone.

- Tightened negative-evidence rules: sparse or 4fps sampling can establish `not_observed`, not interval-level absence; negative facts require bounded scope plus fact-type-appropriate continuous video/audio review or direct counterevidence.
- Added fact-type-specific evidence conflict handling; dialect / strong-accent ASR defaults to locator-only until verified.
- Hardened `ready_for_render` gates: completed Broad/Content Map/Detail stages, both Direct documents confirmed, selected Deep evidence not pending/contradicted, and explicit render authorization are now mechanically checked.
- Validator and compiler now share cumulative timeline quantization and post-overlap output coordinates; text/audio tracks are checked against final output length, not assembly length.
- `source.time_mapping` is included in precise cache identity, so mapping changes invalidate unit / clean-video / audio / final cache keys.
- Added a canonical time-tag policy from source evidence through assembly/output coordinates, with source/time consistency checks.
- Added source usable-boundary propagation into Direct, long-task incremental checkpoint / resume rules, a frame-based duration budget ledger, feedback-to-invalidation mapping, and explicit audio narrative roles.

- Restored the full Board/Broad → Detail Structure information floor: frame-end timing, original-audio keypoints, topic judgment, confidence + evidence basis, detail interval cards, minimum-effective-unit candidates, and frame-level speaker/addressee adjudication.
- Structure summaries, Content Map, editorial copy, or edit plans are explicitly forbidden from replacing these base observation artifacts.

- Restored the Structure minimum-information floor as a hard requirement: one structured row per analyzed sampled frame, with visible facts, action/state, motif tags, hard text, change-from-previous, content description and unknowns preserved before summaries.
- Added `assets/action-node-candidate-template.csv` for action / gaze / position / object-change candidates with default 4fps local inspection windows.
- Added `assets/structure-question-template.csv` for question → answer → evidence → unresolved-item tracking.
- Expanded Deep Observation with key visual changes, emotional cues / interpretation, motif tags, question refs and unverified items.
- Strengthened validation and QA so Content Map / final copy cannot substitute for the foundational Structure layer.
- Rebalanced the README first screen so the project presents **Structure + Execute** as the two core capabilities, with Human Direct as the creative interface between them.
- Repackaged the README around the core value of Structure: turning expensive multimodal source material into compact, searchable and reusable structured data.
- Added a clear before / after explanation and a concrete content-performance example that joins time-coded user behavior with structured visual / narrative observations.
- Added `examples/content-performance-analysis.md` to show how the same structured layer can support analytics and research beyond editing.
- 强化 Structure 的核心定位：把视频 / 图像 / 对白 / 场景上下文等高成本多模态输入压成 **compact structured representation**，供后续人和模型优先通过表格 / 文本低上下文复用。
- 明确 Direct 可在独立研究 / 编导环境中结合 Structure 输出、行业 / 主题资料、平台语境、参考案例与大量人工判断形成并确认 editorial / script plan。
- 明确计算成本策略：Broad Structure 低密度全局压缩；只有已确认脚本命中的区域才进入 Directed Deep Structure 高密度多模态回查。
- `project.json` 增加可选的 `research_context_refs` 与 `human_decision_refs`，用于保留外部研究和人工决策来源。
- 更新 README、Skill、workflow、data contracts、agent metadata 与时间轴校验 / 编译实现；保持 renderer-neutral 架构、正式 Structure / Direct 表单与 render-audit 脚本不变。

## v1.0.1 — Structure observation layer restored

- Restored a formal human-readable **Frame Observation Index** for Broad Structure instead of leaving downstream users with only contact sheets / raw frame evidence.
- Added `assets/frame-observation-template.csv`.
- Added a formal **Deep Observation Index** for Directed Deep Structure.
- Added `assets/deep-observation-template.csv`.
- Expanded Directed Deep Structure to capture complete visual description, content description, setting context, narrative context, before / after state, dialogue / audio verification, interpretations, unknowns and counterevidence before cut decisions.
- Updated README, workflow, data contracts, worked example, handoff rules and agent metadata accordingly.
- No change to the core Direct boundary, timeline compiler, renderer-neutral architecture or render-audit scripts.

## v1.0.0 — Initial workflow

- Broad Structure → Human Direct → Directed Deep Structure → Execute.
- Content Map / Brief / Editorial Plan templates.
- Evidence and timeline contracts.
- Render-manifest compiler and render audit tooling.
- MIT License.
