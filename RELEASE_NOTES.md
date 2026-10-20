# v1.3.1 — AI Video Editing Agent Skill · Visual Methods + Blender Production

日期 / Date: 2026-10-20

**Long Video Remix** turns long-form video into searchable structure, human-directed edit plans, Visual Methods, editable Blender motion composition, FFmpeg rendering, and playback QA for Claude Code and Codex.

核心路径保持：`Broad Structure → Direct 1 → Detail Structure → Direct 2 → Execute → QA`。v1.3.1 强化的是 Direct 2 的视觉方案生成与兜底，不增加新的工作流阶段。

## 中文

v1.3.1 不削弱 v1.3.0 已验证的制作链：Blender 可编辑工程、静态 Proof、连续 Dynamic Demo、FFmpeg 回接和最终真实播放 QA 全部保留。新增的是 Direct 2 的视觉方案能力：Style System + Visual Router + M01–M14 完整方法库 + F01–F09 兜底组合。已有方案时用于校正和深化；Director 仍只有“高级 / 电影感 / 综艺感 / 大字 / 放大”等抽象想法，或真实关键帧使原方案无法落地时，必须从当前视觉问题出发提出可制作候选、比较取舍，再进入 Mockup。

本版采用“瘦加载，不瘦知识”：默认只读 Router，命中后读取完整方法；研究来源和扩展说明仍随包保留，但不进入每轮默认上下文。Visual Methods 不新增阶段、Gate、schema 或 QA 层；现有 schema 1.9、方法 / Composition / Proof / Plan 状态和执行完整性契约保持。默认交互可把多个已展示的确认项合并为 D2 Design Lock 与 Production Proof Lock 两轮，内部仍逐项保存 digest 与 stale 状态。

新项目模板用 `PM001...` 表示当前视频的 Project Method，`M01–M14` / `F01–F09` 只作为知识库引用；旧项目无需迁移原 method ID。

## English

v1.3.1 keeps the production gains of v1.3.0 intact: editable Blender compositions, static proof frames, continuous motion demos, FFmpeg return, and final playback QA remain required. The new layer strengthens Direct 2 visual reasoning with a Style System, a Visual Router, fourteen full methods and nine fallback recipes. It can refine an existing plan or propose executable alternatives when the current plan is generic, abstract, or incompatible with the real keyframes.

Progressive disclosure reduces context cost without deleting the knowledge: read the Router first, then the full matched method. Research/source notes remain available on demand. No new workflow stage, gate, schema, or QA layer is introduced. Schema 1.9 and the v1.3.0 engineering contracts remain compatible.

See [visual production](references/visual-production.md), [Style System](references/style-system.md), [Visual Router](references/visual-methods/index.md), and [release QA](docs/qa/v1.3.1-QA.md).

---

# v1.3.0 — Visual methods, Blender engineering & motion-proof gates

日期 / Date: 2026-10-18

新增制作方法决策、Blender 局部合成、连续动态验证和 FFmpeg 回接；原音乐、Mockup、Proof、D2、范围、授权与 QA Gate 保留。新项目 schema 1.9，旧数据不重扫。完整交付、运行命令和能力边界见 [视觉制作](references/visual-production.md)，实际回归见 [本版 QA](docs/qa/v1.3.0-QA.md)。

Adds narrative-led method decisions, editable Blender compositions, continuous motion review and a return to the existing FFmpeg pipeline. Engineering/render success never auto-confirms a user decision or final QA. Both source formats share the complete core. Blender and third-party MCP programs are separate dependencies.

---

# v1.2.5 — Workflow control & chat continuation / 阶段内关口与 Chat 续接

日期 / Date: 2026-10-18

## 中文

v1.2.5 不改变 Broad Structure → Direct 1 → Detail Structure → Direct 2 → Execute → QA，也不新增创作阶段。它把原本分散的确认和续接状态统一记录到 `project.json.workflow_control`：同一项目继续、换会话或局部修改时先恢复有效 / 待确认 / 已失效关口；声音策略、Mockup、Proof、计划与证据只在输入发生相关变化时重新打开。授权草稿和 `ready_for_render` 接入这些检查，partial handoff 会保留未过关口；旧项目可用 `workflow_control.py init` 补控制记录，不重扫素材、不自动确认。最终 QA 继续绑定实际成片指纹。

## English

v1.2.5 keeps Broad Structure → Direct 1 → Detail Structure → Direct 2 → Execute → QA unchanged and adds no creative stage. It consolidates continuation and confirmation state into `project.json.workflow_control`: resuming the same project, switching chats, or making a local revision restores satisfied / pending / stale gates first, and audio strategy, mockup, proof, plan, and evidence reopen only when relevant inputs change. Authorization drafts and `ready_for_render` checks consume this state; partial handoffs retain every open gate. Existing projects can run `workflow_control.py init` to add control records without rescanning media or auto-confirming decisions. Final QA remains bound to the actual rendered artifact fingerprint.

---

# v1.2.4 — Gate & Compatibility Hardening / Gate 与兼容性加固

Date / 日期: 2026-10-17

## 中文

v1.2.4 不新增创作阶段，主要修复 v1.2.3 发布前暴露的工程漏洞。

- **Git 安装校验修复**：`tests/test_checksums.py` 只核对 `SHA256SUMS` 中声明的文件，不再把 `.git/`、`.DS_Store` 等本地元数据误判为包内容；新增 `.gitattributes`，仓库文本统一 LF，减少 Windows clone 后 checksum 漂移。
- **schema 1.7 兼容性恢复**：v1.2.3 的“partial boundary 可延后最终音画精校”只适用于 schema 1.8+。schema 1.7 继续沿用 v1.2.2 的边界严格度，不因升级 Skill 意外变松。
- **版本号严格解析**：`validate_project.py` 与 `execution_integrity.py` 共用 `scripts/versioning.py`。`project.schema_version` 只接受 `1.8` 这类纯数字点号格式；`v1.8`、`1.8-rc1` 等直接报错，不再静默退回旧规则。
- **capability-map 契约统一**：文档统一为 `{schema_version, capabilities:[...]}` 对象。Visual Gate=`proof_confirmed` 时，不再接受任意 available capability；必须有一条 capability 同时具备真实 `actual_tool + entrypoint`，且 `output_mapping` 实际指向当前 `visual_proof_ref`。
- **Step 0 上游边界可机器核对**：schema 1.8 的 source event 新增轻量 `d2_selection_snapshot`，保存 D2 planned in/out、selected boundary、当时 safe windows 与允许的 trim / handle 调整。Execute Step 0 只能在该快照内校准；扩大 safe windows、替换 boundary 或超出允许范围时必须停止并返回确认。
- **授权仍沿用原体系**：不新增授权 schema。`prepare_execution_authorization.py` 会把 snapshot 中的 allowed adjustments 带入 draft；最终 event spec、evidence 和 reference 指纹继续由现有 authorization 锁定。

## English

v1.2.4 hardens the v1.2.3 release path without adding another creative stage.

- **Git-install checksum fix:** checksum regression now verifies only files declared in `SHA256SUMS`, so `.git/`, `.DS_Store`, and other local clone metadata do not fail installation verification. `.gitattributes` pins repository text to LF to reduce Windows checksum drift.
- **Schema 1.7 compatibility restored:** deferred precision for `partial` boundaries applies only to schema 1.8+. Schema 1.7 retains the stricter v1.2.2 boundary behavior.
- **Strict shared schema parsing:** `validate_project.py` and `execution_integrity.py` share `scripts/versioning.py`. Only dotted numeric values such as `1.8` are valid; `v1.8` and `1.8-rc1` are errors rather than legacy fallbacks.
- **Capability-map contract aligned:** documentation now matches the actual `{schema_version, capabilities:[...]}` object. `proof_confirmed` requires an available capability with real `actual_tool + entrypoint` whose `output_mapping` resolves to the current `visual_proof_ref`.
- **Machine-checkable Step 0 envelope:** schema 1.8 source events carry a compact `d2_selection_snapshot` containing D2 planned in/out, selected boundary, the then-current safe windows, and allowed trim / handle adjustments. Execute Step 0 may calibrate only inside that snapshot; widening the envelope or switching the boundary stops for confirmation.
- **Authorization remains the same system:** no new authorization schema is introduced. Draft authorization inherits snapshot adjustment permissions, while the existing event-spec, evidence, and reference fingerprints lock the confirmed result.

## Verification / 验证

- **216 regression tests passed.** In this build environment, the non-extraction suites and the 11 FFmpeg extraction tests were run in smaller batches; every discovered test passed.
- `examples/synthetic-ready`: validation, render-manifest compilation, authorization check, and deterministic visual-proof regeneration passed under schema 1.8.
- Verified environment: Python 3.13.5, FFmpeg 7.1.5, Pillow 12.3.0.
- `SKILL.md` and `references/workflow.md` remain within their existing size budgets.
- No real long-video end-to-end performance benchmark was added in this release.
