# 安装与更新 · v1.3.1

Long Video Remix 是面向 Claude Code 与 Codex 的 **AI video editing Agent Skill**，覆盖 long video to shorts、video highlights、Visual Methods、Blender motion composition、FFmpeg rendering 与 QA。

本版沿用 v1.3.0 的 [制作方法、Blender 合成与动态验证](references/visual-production.md)，并加入 [Style System](references/style-system.md) / [Visual Router](references/visual-methods/index.md) 作为 Direct 2 的视觉方案生成与兜底知识层；不新增阶段、Gate、schema 或 QA。完整保留原文件；新项目复制 project-template（schema 1.9），填方法/合成/delivery 三个模板。静态脚本需 Python 3.9+，实际局部合成需安装 Blender，回接需 FFmpeg/ffprobe。Blender/MCP 不打进 ZIP，也不因解压自动可用；无执行能力时 Gate 保持 pending。实际 Linux 渲染、回归和未验证项见 [本版 QA](docs/qa/v1.3.1-QA.md)。

旧项目要采用新管线先运行 `python scripts/visual_pipeline.py init PROJECT`；承接证据、范围和有效确认，不重扫。已有 schema 1.8 项目可维持原流程；不能在采用新管线后通过降级 schema 或删除 policy 规避确认。

解压后得到 `long-video-remix/` 完整目录。SKILL.md、references、assets、scripts 和 agents 必须一起保留；只复制 SKILL.md 会丢失契约和检查能力。

## 安装

使用本地 Claude Code 或 Codex 时，选择对应命令。以下命令用于首次安装；已有同名目录时先备份，再更新或替换完整文件夹。

```sh
# Claude Code
mkdir -p ~/.claude/skills && git clone https://github.com/hazelliuliu1823-cloud/long-video-remix.git ~/.claude/skills/long-video-remix

# Codex
mkdir -p ~/.agents/skills && git clone https://github.com/hazelliuliu1823-cloud/long-video-remix.git ~/.agents/skills/long-video-remix
```

解压安装包时，也可将完整 `long-video-remix` 文件夹放入 `~/.claude/skills/`（Claude Code）或 `~/.agents/skills/`（Codex）。项目素材和工作数据放在独立项目目录，不放进安装目录。

用 Git 安装的副本可在安装目录执行 `git pull --ff-only` 更新。仓库安装获取当前分支版本；需要固定 v1.3.1 时，可使用对应安装包，或在 Release/tag 发布后执行 `git clone --branch v1.3.1 --depth 1 <repo> <目标目录>`。安装或更新后检查工具的技能列表。

目录依据：[Claude Code 本地 skills](https://code.claude.com/docs/en/skills) · [Codex 本地 skills](https://learn.chatgpt.com/docs/build-skills)，核对日期：2026年10月2日。

这是 Skill 与配套脚本安装包。画面读取、ASR、实际渲染通过当前环境的模型、视频 MCP 或渲染器连接，按 references/mcp-adapter.md 发现并验证能力。

## 运行环境

- 静态校验、授权记录、编译与回归：Python 3.9+，只用标准库。
- 抽帧与时间信号（`extract_frames.py`）、导出审计：FFmpeg / ffprobe；生成拼图时额外需要 Pillow。
- 模型、视频 MCP、渲染器的依赖按实际适配器配置，不在包内下载大模型或素材。

Python 3.9 已做语法兼容检查，尚未在 3.9 解释器上实际运行回归；v1.3.1 当前回归环境为 Python 3.13.5 + FFmpeg 7.1.5 + Pillow 12.3.0，共发现 265 项测试：263 通过、2 项因本轮未配置 `BLENDER_EXECUTABLE` 而条件跳过、0 失败。v1.3.0 QA 保留此前真实 Blender/FFmpeg 合成素材渲染验证；v1.3.1 不把该历史验证冒充成本轮重跑。缺少 FFmpeg / Pillow / Blender 时，对应集成测试会按条件跳过。

## 验证安装包

进入解压后的目录运行：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_project.py examples/synthetic-ready
python3 scripts/compile_render_manifest.py examples/synthetic-ready
python3 scripts/check_render_authorization.py examples/synthetic-ready examples/synthetic-ready/render-manifest.json
```

示例全部是合成记录，只验证数据链与工程入口；没有真实视频，不用它证明长视频理解或观看效果。

## 从 v1.2.3 更新

- 不新增阶段、正式 CSV header 或授权 schema。schema 1.8 项目的 Direct 2 现在把 planned in/out、selected boundary、当时 safe windows 和允许调整写进 timeline source event 的 `d2_selection_snapshot`；Execute Step 0 只能在该快照内校准。越界、扩大 safe windows 或换 boundary 时停止并返回确认。
- schema 1.7 恢复 v1.2.2 的旧边界严格度：即使 boundary 标为 `partial`，dialogue / action / reaction / mixed 等适用连续性仍按旧规则要求精确值；只有 schema 1.8+ 才允许未入选候选把最终精校延后。
- Visual Proof 的 capability 不再是任意 available tool：`output_mapping` 必须实际指向当前 `visual_proof_ref`，并同时具备 `actual_tool + entrypoint`。
- `project.schema_version` 只接受 `1.8` 这类纯数字点号格式；`v1.8`、`1.8-rc1` 等直接报错，不再退回旧规则。
- `SHA256SUMS` 测试只核对 manifest 中声明的文件，因此 Git clone 产生的 `.git/` 或本机 `.DS_Store` 不再导致安装验证失败；仓库新增 `.gitattributes` 固定文本 LF，减少 Windows clone 后的 checksum 漂移。

## 从 v1.2.2 更新

- 新项目模板使用 project schema 1.8；不新增正式 CSV header。
- Detail 的 dialogue / mixed / action 候选可先以 `boundary_status=partial` 交付 selection-ready 保守边界；没有必要提前完成最终尾音 / settle 精校。
- Direct 2 输出 planned range + boundary ref；回到实际执行环境后先做 Execute Step 0，只精校 D2 已选 range + handles。schema 1.8+ 到 `ready_for_render` 时，入选 boundary 必须为 `supported`。
- 完整 ASR 不再是 Detail 完成条件；使用可靠字幕 + signals / waveform 定位，ASR 按需跑小窗口。
- Step 0 后再按最终 source in/out 准备 / 确认 execution authorization。schema 1.7 项目可继续按 v1.2.2 行为运行，无需强制迁移。

## 从 v1.2.1 / v1.2.0 更新

更新完整安装目录即可；A–G、两次 Direct 和正式 CSV 表头不变。本版把 `project.json` schema 从 1.6 升到 1.7，仅用于区分“新项目必须经过 Visual Gate”和旧项目兼容行为；不新增 `current-state.json`、`visual-style.json` 或 Music Gate。

- **Scope Lock**：在 Narrative Direction、Detail handoff、Execution Plan 的现有模板中只写四行：当前阶段、可修改、不可修改、已否决。
- **Detail STOP**：目标问题、最小完整互动 / 动作单元、Edit Boundary、相关反证四项闭合后停止继续加密读取。
- **Visual Gate**：schema 1.7 新项目必须使用 `execution_package_policy=plan_and_reference`，且 `project.json` 必须包含 `visual_gate_status`、`visual_mockup_ref`、`visual_proof_ref`。先确认 Aesthetic Mockup；随后可在另一模型 / 会话中，用最终 Execute 可访问的同一实际工具链生成 Executable Proof。`capability-map.json` 继续是唯一工具映射来源，可从 `assets/capability-map-template.json` 建立；可执行 capability 记录 `actual_tool + entrypoint`。
- `visual_gate_status` 可为 `not_started`、`mockup_confirmed`、`awaiting_proof`、`proof_confirmed`、`not_applicable`。ready_for_render 只接受 `proof_confirmed` / `not_applicable`；proof_confirmed 时 mockup 与 proof 必须是路径和内容都不同的两个实际文件；二者与 `capability-map.json` 一起进入 `execution_reference_asset_refs`，且 capability-map 至少有一个 available capability 记录真实 `actual_tool + entrypoint`。
- 如果现有执行工具链无法复现已选 mockup，不要用下游不可用的工具临时生成 proof；保持 Gate open，调整 mockup，或正式更新 capability-map / execution-reference / 最终 Execute 路径后重做 proof。

schema 1.6 旧项目没有这三个 Visual Gate 字段时继续保持兼容行为；迁移到 1.7 时补齐字段、capability-map 与 proof 即可，不要求重扫 Broad / Detail。随包 `examples/synthetic-ready` 已演示完整 1.7 流程。

## 从 v1.1.0 更新

更新完整安装目录，保留已有项目数据、真实关键帧和已确认叙事。v1.2.0 更新交付规范与模板，沿用现有脚本、正式 CSV 表头及 schema：Detail 单独保存并交付关键帧原图；Direct 2 用真实关键帧制作完整画面 mockup，随 Execution Package 交付设计参数、必要资源和可复用布局入口；Execute 用同一套参数制作，再核对成片与 mockup 风格是否匹配（不要求逐帧或逐像素对应）。通常一两个代表样稿即可；特殊版式按本次实际使用提供。商用发布时注意字体授权。进入 ready_for_render 时若未登记任何 mockup / 参考图，validator 会给出提醒但不阻断。

已有执行包要采用本版规范时，补齐上述实际文件和入口；缺失项标待补，不把参数表算作已完成 mockup。设计或样稿变化沿用既有 Direct 2 授权流程。详见 [执行包规范](references/execution-package.md)。

## 从 v1.0.7 更新

v1.1.0 以 v1.0.7 为底，只加四件事，不改正式 CSV 表头，不新增创作阶段：

1. **抽帧标签实测。** 本地原片且 identity 映射时优先用 `scripts/extract_frames.py`；MCP / 代理等按 [MCP 适配](references/mcp-adapter.md) 保留实测时间与源绑定，不改写既有映射。脚本的 `signals` 模式输出变化与声音候选，`strip` 输出逐帧条。旧版输出重抽时使用新目录；普通帧索引不能作为清空目录的许可。
2. **Detail 取证规则。** 新增 `references/detail-evidence.md`（只在 E 阶段读取）：全覆盖、按内容定密度、每个时间点只读一次；细动作不凭缩略图下结论；切点先夹住再逐帧；密集读图不拆给子代理。
3. **两道门槛。** Detail 文件一出现，`validate_project.py` 就做结构检查。Detail 完成时，`target_questions` 必须是稳定 `question_id` 并被观察回指；`contradicted / unresolved` 问题列入 handoff 的 Question Closure Ledger；入选成片的节点不得带 `unresolved`，带 `contradicted` 须有人工 `confirmed_by`。
4. **SKILL.md 大小上限。** `tests/test_size_budget.py` 把 SKILL.md 限制在 v1.0.7 的大小以内，新增规则须先删等量内容。

**项目迁移。** 以下各项只在 Detail 标记完成时检查；建议迁移后先运行一次 `validate_project.py`，按报错逐条处理：

1. **稳定问题 ID。** v1.0.7 的 `target_questions` 若是自由文本，先在 `structure-questions.csv` 建立唯一、稳定的 `question_id`，把区间改为引用 ID，并在实际回答它的观察里写 `question_refs`。
2. **观察与区间的节点一致。** `deep-observations.plan_node_id` 必须等于它所在 `detail_interval_id` 的 `plan_node_id`。服务于另一个节点的观察，应放进那个节点的区间。
3. **问题与关联区间一致。** 问题行里写了具体值（不是 `none` / `unknown` 等）的 `source_id`、`plan_node_id`、`detail_interval_id`，必须与它实际关联的区间一致；问题的 `detail_interval_id` 也必须是存在的区间。一个问题同时关联多个区间时，`detail_interval_id` 写 `none`；这些区间的节点不同时，`plan_node_id` 也写 `none`。
4. **问题闭环表。** 已有 handoff 若有被否决 / 未解决的问题，补上 Question Closure Ledger 表（模板见 `assets/execution-handoff-template.md`）。表格放在包含 "Question Closure Ledger" 或"问题闭环"字样的标题下，可附中文说明；每个问题只列一行，`plan_node_id` 写它实际关联的全部节点（多个用分号分隔）。

用 v1.0.7 习惯手工抽的帧，若标签是"起点 + 序号 × 间隔"算出来的，进入精确切点前请用脚本或已验证适配器重新取得实测标签。

## 从 v1.0.8–v1.0.10 更新

v1.1.0 不沿用 v1.0.8–v1.0.10 的开发线，而是回到 v1.0.7 重建。对用这些版本建立的项目：

- 稳定 question ID、`question_refs` 显式回指：保留，无需改动；上面第 2、3 项一致性规则同样适用。
- `extract_detail_evidence.py`、`detail_progress.py`、`detail-evidence-state.json`、semantic draft / `compile_detail.py`、`prepare_detail.py`：不再提供。抽帧改用 `extract_frames.py`（实测标签；v1.0.10 的抽帧标签比画面早约半个采样间隔，需重新抽取）。
- `narrative-conflicts.jsonl`、D1 重新确认文件：由 handoff 的 Question Closure Ledger 取代。把其中的处理方式与确认人填入该表即可；旧文件不再被读取。
- 五个 Detail `structure_policy` 常量：不再使用，保留也会被忽略。

## 从 v1.0.6 更新

本次为双语使用示例与发布文档更新。更新完整安装目录即可，工程脚本、正式表单和项目 schema 保持原样；已有项目资料和已确认方案继续复用。四个常用提问示例位于中英 README 的“快速开始”之后。

## 从 v1.0.5 更新

保留已有项目、六套正式 CSV 表头和观察数据。按 v1.0.7 继续工作时，Structure 无法取得的字段通过 `structure-exceptions.jsonl` 明确声明，继续可做部分；Detail 交付 `keyframe-references.json`、可取得的真实图片与 `execution-handoff.md`（直接含下游完整交付要求）。

Direct 2 同时提供 `execution-plan.md` 与 `execution-reference.md`。project 增加对应 refs、`execution_reference_asset_refs`（无图片时 []）与 `execution_package_policy="plan_and_reference"`。reference 使用一两个样本锁定整体风格，不逐镜头配对。已有授权流程追加 reference 文档 / 样本指纹，按已有确认更新 draft / 授权并重新编译；不重做已核实的原片观察。

旧项目未声明新 policy 时保持原机械行为；新 policy 的文件 / 指纹检查不替代执行包内容审阅和最终 Reference Compliance。无法提取关键帧可明确异常后继续，但未核实证据、缺失源时间及完整对白保护仍按原规则处理。完整契约见 [执行包规范](references/execution-package.md)。

## 从 v1.0.4 更新

保留 Structure 文件与全部正式表单。程序现在逐条 source_id 音轨推导实际取段内已知对白，卡片对白、未关联音轨和另一素材仅采用声音均接受整句证据与保留政策检查，不要求为独立声音补造视频 event 或 Edit Boundary。

独立对白轨使用 kind=original、narrative_role=dialogue_information、treatment=preserve / isolate，并确定 gain、fades、speed 和成片位置。anchor_event_id 只决定放置位置；它不声明口型同步。需要同步的视频原声仍填写对应 source event 的 audio_source_refs 和 sync_event_id / sync_mode。

每条源音轨可选写 adopted_utterance_refs，写时须是唯一 ID 数组；实际取段内已知对白始终自动加入检查，[] 不会免检。保留政策下的独立删句 / 截尾，使用 track.overrides 的 audio_required_range，target_id 为 track_id，范围覆盖受影响整句且有当前有效整句核听。明确改为 preserve_dialogue=false 时，独立对白轨填写具体 dialogue_policy_reason；已关联视频对白沿用 event 级原因及例外，不要求重复填写。

独立音轨采用的 utterance 和专属 review 现在进入 evidence_digest。完成实际证据与已有创作决定对账后，用准备 draft 的既有流程更新 Direct 2 授权和 project 指纹，再重新校验、编译；不能直接把旧摘要当作当前确认。完整对白合法方案继续适用，详见 [执行完整性契约](references/execution-integrity.md)。

## 从 v1.0.3 更新

保留已有结构化数据和正式表单，只补执行记录：source event 增加 `adopted_utterance_refs`（明确采用的 utterance ID；没有时写 []），每条源音轨增加独立 `review_refs`。核听记录须覆盖音轨完整的 source_in_ms—source_out_ms，包括 J/L-cut 扩展部分，且来源、版本与音频模态有效。仅核听过视频取段，不能代替扩展音轨的核听。

程序还会从实际选用的视频及全部源音轨推导应保护的已知对白；缩小 dialogue_required_range 或清空采用列表不能让取段内对白消失。scene / action 等标签仍须遵守保留对白政策。若本轮已明确改变为不保留对白，更新 audio_policy，并在对应 event 或独立音轨写入具体 `dialogue_policy_reason`；保留政策下的删句 / 截尾使用具体的 audio_required_range 创作例外。

补齐真实核查与已确认决定后，再更新 Direct 2 机器授权和 project 中的授权指纹，重新校验、编译。不要只改指纹来替代核听。详见 [执行完整性契约](references/execution-integrity.md)。

## 从 v1.0.2 或更早版本更新

保留已有项目，不重做 Broad。采用 Deep / boundary / review / unit.verification / utterance 需要保存实际核实时的源版本与映射指纹；补 source event 和源音轨的绑定、源许可与声音映射。按 Direct 2 已确认方案准备 execution-authorization.json，并把其指纹记入 project。完整规则见 [执行完整性契约](references/execution-integrity.md)。

旧项目进入正式执行前须完成这些字段，并按上节补充对白采用与完整音轨核听记录；缺少时会被阻断。指纹工具不会替旧资料伪造重新审阅，也不会自动确认草稿。
