# Detail Structure → Director 2 Handoff

> E 阶段交付。接收方无需安装原 Skill，即可凭本文件与随附证据形成 Execution Package。本文件不替代 Detail 表，也不提前生成最终剪辑方案。模板空白须填入实际信息；未知项明确标注并带异常原因。

## 当前状态与文件清单

- 项目 / 产物版本：
- 当前已完成范围 / coverage 缺口：
- 实际随附文件与可读取位置（包括图片）：
- 尚未包含的资源与取得方式：
- exceptions 文件及影响 / 下游处理：

## 已确认叙事背景

- Narrative Direction 文件与确认来源：
- 核心主题 / 内容目标：
- 情绪路径 / 人物关系（事实、解读分列）：
- 必须保护的原话、画面、动作与表达重点：
- 已确认禁改项：

## 所选素材与证据

| segment / unit ID | source ID / 版本 / time_mapping | 源区间 ms | 叙事用途及状态 | evidence refs / reviews | context / protected ranges | edit boundary / safe windows | 缺口 / 反证 |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

原音轨完整核听范围、问答 / 动作的最短完整范围及切点风险：

### Question Closure Ledger

所有 `answer_status=contradicted` 或 `unresolved` 的 Detail 问题逐行列出；没有时保留表头。标题可附中文说明，但须包含 "Question Closure Ledger" 或“问题闭环”字样，validator 只读取这个标题下的表格。每个 question_id 只列一次，plan_node_id 与实际关联节点一致（多个节点用分号分隔）。`处理方式` 写具体下游动作（不能只写 resolved）；入选成片的节点带 `contradicted` 问题时，`confirmed_by` 必须是作出该决定的人。

| question_id | status | plan_node_id | 处理方式 | confirmed_by |
|---|---|---|---|---|

## 原片关键帧

- keyframe-references.json：
- 单独保存、实际随包附带的原片关键帧图片与 source timestamp：
- 每张图对应的素材节点 / narrative role：
- 提取失败或定位不确定项（status / reason / impact / downstream_handling）：

## 下游任务：生成完整 Execution Package

Director 2 基于以上已核实素材和 Narrative Direction 决定最终呈现；保留两次 Direct 的职责，不重做已确认主线，不把未核实项当成事实。素材不足只补对应缺口；主线冲突说明证据并返回 Direct 1。

请一次交付以下内容，已明确的规则填具体参数，不将必要判断留到 Execute：

1. **Editorial Execution Plan / execution-plan.md**：最终素材取舍、顺序、逐段 source in/out、速度 / 画面处理、保护范围、时长预算、逐条文字全文与出现 / 消失锚点、原声音轨及接点处理。
2. **Visual / Text Reference / execution-reference.md**：字体及可用资源、字号与单位、字重 / 颜色、位置 / 对齐、换行 / 行数、描边 / 背景、阅读停留、动效；明确输出分辨率、原片裁切 / 缩放和文字与画面的关系。
3. **Audio Specification**：每条原声 / 环境音 / BGM / 旁白的政策、源取段、成片放置、增益、速度、淡化、完整对白保护；没有配乐需求时不默认添加。
4. **Transition Specification**：每个接点采用什么及帧数；黑场 / card / hold 若增时，要计入事件与总长。
5. **Mockup（锁定风格）**：用随附真实关键帧、实际文字和目标输出画幅做一两个可打开的完整画面样稿，锁定全片风格（含本次采用的相片页 / 录像框等版式）；附字体（商用注意授权）、字号、位置 / 边距、裁切与框体等参数及可复用生成入口，说明哪些标记实际进入视频。执行沿用同一套设计，不逐镜头映射。缺原图或出图能力时标待补并先交参数；依赖该视觉的制作前补齐可查看样稿。
6. **Asset / Constraints**：可读素材、证据、关键帧、字体和参考资源；允许调整、禁改项、status / reason / impact / downstream_handling。封面等仅在本任务要求时提供，其余记 not_applicable。
7. **QA Criteria**：内容、保护范围、时间、文字可读性、音轨 / 接点与 Reference Compliance（成片与 mockup 风格匹配即可，不要求逐帧或逐像素对应）。静态检查和真实播放分开，未实看写 not_tested。
8. **原有机器授权**：已有项目继续使用 execution-authorization.json，保存采用范围、顺序、允许调整与证据 / 决策指纹；草稿不自动升为 confirmed。reference 文档 / 实际样本改变后，旧确认失效，须按已有授权裁决并更新。

时间继续以 source_id + source ms 定位，文字 / 音轨放置优先使用 event anchor + local frames；正式成片坐标按现有时间轴编译对账。异常可以随包继续推进可做部分，但不能豁免证据、完整对白、Edit Boundary、源许可或正式渲染条件。

## Execute 接手入口

接收 Source Clips + Detail Structure + execution-plan + execution-reference + Constraints 组成的完整包。按已确认方案和允许调整制作；不重新选择核心主题、取舍或风格。资源 / 参数仍有缺口时先明确处理，不擅自补造确认结果。
