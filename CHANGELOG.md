# Changelog

## v1.0.2 — Compact multimodal structure for lower-context reuse

- Repackaged the README around the core value of Structure: turning expensive multimodal source material into compact, searchable and reusable structured data.
- Added a clear before / after explanation and a concrete content-performance example that joins time-coded user behavior with structured visual / narrative observations.
- Added `examples/content-performance-analysis.md` to show how the same structured layer can support analytics and research beyond editing.
- 强化 Structure 的核心定位：把视频 / 图像 / 对白 / 场景上下文等高成本多模态输入压成 **compact structured representation**，供后续人和模型优先通过表格 / 文本低上下文复用。
- 明确 Direct 可在独立研究 / 编导环境中结合 Structure 输出、行业 / 主题资料、平台语境、参考案例与大量人工判断形成并确认 editorial / script plan。
- 明确计算成本策略：Broad Structure 低密度全局压缩；只有已确认脚本命中的区域才进入 Directed Deep Structure 高密度多模态回查。
- `project.json` 增加可选的 `research_context_refs` 与 `human_decision_refs`，用于保留外部研究和人工决策来源。
- 更新 README、Skill、workflow、data contracts、brief / editorial plan 模板和 agent metadata；不改时间轴编译、renderer-neutral 架构或 render-audit 脚本。

## v1.0.1 — Structure observation layer restored

- Restored a formal human-readable **Frame Observation Index** for Broad Structure instead of leaving downstream users with only contact sheets / raw frame evidence.
- Added `assets/frame-observation-template.csv`.
- Added a formal **Deep Observation Index** for Directed Deep Structure.
- Added `assets/deep-observation-template.csv`.
- Expanded Directed Deep Structure to capture complete visual description, content description, setting context, narrative context, before / after state, dialogue / audio verification, interpretations, unknowns and counterevidence before cut decisions.
- Updated README, workflow, data contracts, worked example, handoff rules and agent metadata accordingly.
- No change to the core Direct boundary, timeline compiler, renderer-neutral architecture or render-audit scripts.

## v1.0.0 — Initial public release

- Broad Structure → Human Direct → Directed Deep Structure → Execute.
- Content Map / Brief / Editorial Plan templates.
- Evidence and timeline contracts.
- Render-manifest compiler and render audit tooling.
- MIT License.
