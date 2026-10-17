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
