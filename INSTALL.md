# 安装与更新 · v1.2.2

解压后得到 `long-video-remix/` 完整目录。SKILL.md、references、assets、scripts 和 agents 必须一起保留；只复制 SKILL.md 会丢失契约和检查能力。

## 本次确认节点修订

本包保留 v1.2.2 版本号，补齐声音形式、实际 Mockup 与整包的确认要求。模板新增 visual-confirmation；校验器要求样稿可解码、尺寸匹配、原图可达、参数同版并有明确确认来源。缺图 / 未确认时可继续证据与 --planning 草案，正式渲染阻断。采用配乐时另核对实际文件、区间与有效 Music Map。图片解码按需使用 Pillow，非 PCM WAV 音乐时长检查使用 ffprobe；能力缺失先保留草案。下文历史版本说明保留当时行为，本包正式执行以 [执行包契约](references/execution-package.md) 为准。

## 安装

使用本地 Claude Code 或 Codex 时，选择对应命令。以下命令用于首次安装；已有同名目录时先备份，再更新或替换完整文件夹。

```sh
# Claude Code
mkdir -p ~/.claude/skills && git clone https://github.com/hazelliuliu1823-cloud/long-video-remix.git ~/.claude/skills/long-video-remix

# Codex
mkdir -p ~/.agents/skills && git clone https://github.com/hazelliuliu1823-cloud/long-video-remix.git ~/.agents/skills/long-video-remix
```

解压安装包时，也可将完整 `long-video-remix` 文件夹放入 `~/.claude/skills/`（Claude Code）或 `~/.agents/skills/`（Codex）。项目素材和工作数据放在独立项目目录，不放进安装目录。

`v1.2.2` tag / GitHub Release 发布后，推荐从 Releases 下载并解压完整的 github-ready 安装包；用 Git 安装的副本可在安装目录执行 `git pull --ff-only` 更新，开发者可执行 `git checkout v1.2.2` 固定到本版。安装或更新后检查工具的技能列表。

目录依据：[Claude Code 本地 skills](https://code.claude.com/docs/en/skills) · [Codex 本地 skills](https://learn.chatgpt.com/docs/build-skills)，核对日期：2026年10月2日。

这是 Skill 与配套脚本安装包。画面读取、ASR、实际渲染通过当前环境的模型、视频 MCP 或渲染器连接，按 references/mcp-adapter.md 发现并验证能力。

## 运行环境

- 静态校验、授权记录、编译与回归：Python 3.9+，只用标准库。
- 抽帧与时间信号（`extract_frames.py`）、导出审计：FFmpeg / ffprobe；生成拼图时额外需要 Pillow。
- 模型、视频 MCP、渲染器的依赖按实际适配器配置；Release 不捆绑第三方模型权重或大模型。代码、权重与其他可下载资源的许可证分别核对。

Python 3.9 继续保持语法兼容目标；本轮 200 项回归在当前 Python 环境通过，FFmpeg / Pillow 相关能力按实际安装条件运行或跳过。缺少 FFmpeg 或 Pillow 时，抽帧相关测试会跳过。

## 验证安装包

进入解压后的目录运行：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_project.py examples/synthetic-ready
python3 scripts/compile_render_manifest.py examples/synthetic-ready
python3 scripts/check_render_authorization.py examples/synthetic-ready examples/synthetic-ready/render-manifest.json
```

示例全部是合成记录，只验证数据链与工程入口；没有真实视频，不用它证明长视频理解或观看效果。


## 从 v1.2.1 更新

更新完整安装目录即可；不需要另行打包 Demucs、额外音乐分析库、FFmpeg 等第三方程序。v1.2.2 只补齐 capability 缺失时的运行时解析规则，现有 Music Mode、Execution Package、timeline 与授权机制不变。

- 新项目模板增加 `capability_resolution_policy="discover_then_prepare_if_permitted"`。旧项目不填该字段仍可继续运行。
- 任务需要某项 capability 时，先发现并复用当前 MCP / 本地工具；没有时，当前 Agent 若具备终端 / 包管理权限，只能在软件许可证允许当前用途、来源明确且可本地运行时主动准备首选后端并做 smoke test；“免费”本身不等于可商用。
- `separate_dialogue` 可优先解析到 Demucs 兼容本地实现，基础音频抽取 / 混音 / 检查优先复用 FFmpeg / Media；`analyze_music` 继续按抽象 capability 发现许可证兼容的本地或 MCP 实现，不指定额外音乐分析后端。
- Demucs 代码按其官方 MIT License 使用；预训练模型权重与代码许可证分开判断。本 Release 不打包 Demucs 或其他第三方模型权重；商业使用权不明确的权重不得被静默当作可商用资源。
- Demucs / PyTorch 等可能产生较大下载量或改变 Python 依赖图；这类准备先说明下载 / 环境影响，并默认安装到项目独立 venv，不修改用户已有全局 Python，除非用户明确要求。
- 首次获取任何模型权重前，分别记录来源、版本 / 哈希与许可状态；只有许可允许当前用途时才可自动获取并缓存，后续复用。
- 需要付费 API、账号 / token、向第三方上传素材、管理员 / root 提权、修改安全设置、来源不明的软件，或许可证不允许 / 无法确认当前用途时，不能静默准备，按 capability fallback 处理或由用户决定。
- 安装成功不等于能力可用；必须经过最小样本 smoke test 后才能在 capability-map 标记 `available`。

## 从 v1.2.0 更新

更新完整安装目录即可；已有项目如果既不声明 `music_direction_policy`、也不填写 `music_direction_ref`，继续按 v1.2.0 的机械行为运行；一旦填写 ref，即按 fail-closed 进入 Music Mode Gate。新项目模板默认启用 `music_direction_policy="mode_confirmation_required"`，Direct 2 在最终 Execution Package 前增加一次 Music Mode Gate。

- 新增 `music-direction.json`：Director 2 先基于 Narrative Direction + Detail 推荐 `narrative_led / hybrid / music_led`。已有明确用户选择直接承接；否则保持 `proposed`，给出推荐与 A/B/C 并结束当前回合，直到用户明确确认。
- 需要音乐参与组织画面时，可增加 `music-map.json`，保存 BPM / beat / accent / energy / section candidates 与编辑意义上的 Music Map / AV Mapping。
- `execution-plan.md` 增加 Audio Treatment Plan；本轮执行覆盖 preserve / isolate / attenuate / replace / remove / designed silence，以及 gain / fade / duck / mix / normalize。人声分离只按需触发，输出作为 derived asset 保存并核听。
- `mcp-adapter.md` 增加 `extract_audio / separate_dialogue / analyze_music / mix_audio / inspect_audio` 抽象 capability；底层可以是本地程序、MCP 或远程服务，不绑定 Demucs 等具体后端。
- 新 policy 下，未确认的 music mode 会阻断 ready_for_render；music-direction 和已采用 Music Map 进入 Direct 2 授权指纹，确认后修改会使旧授权失效。

旧项目想启用本机制时，在 `project.json` 增加 `music_direction_policy` 与 `music_direction_ref`，按 `assets/music-direction-template.json` 建立决策文件；若声明 `music_map_required=true`，同时提供 complete / verified 的 Music Map。详见 [Sound & Music Execution](references/sound-music-execution.md)。

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
