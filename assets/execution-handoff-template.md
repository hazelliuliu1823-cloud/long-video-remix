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

请按以下顺序交付。先完成 Music Mode Confirmation Gate，再形成最终 Execution Package；已明确的规则填具体参数，不将必要判断留到 Execute：

0. **声音确认 / music-direction.json**：先基于主线与 Detail 推荐 `narrative_led / hybrid / music_led`，同时推荐保留节目混音、仅原声、新增 / 替换配乐或留白的声音形式，写明人声分离与回退、保护 / 可调整区域。已有明确选择直接承接并记录来源；否则先呈现推荐并等待确认，再完成依赖该选择的设计。采用具体配乐时，整包列明曲目、版本、区间、文件与指纹；需要音乐组织画面时附完整 Music Map / AV Mapping。
1. **Editorial Execution Plan / execution-plan.md**：最终素材取舍、顺序、逐段 source in/out、速度 / 画面处理、保护范围、时长预算、逐条文字全文与出现 / 消失锚点、Audio Treatment Plan、必要的 Music Map / AV Mapping、最终音轨及接点处理。
2. **Visual / Text Reference / execution-reference.md**：字体及可用资源、字号与单位、字重 / 颜色、位置 / 对齐、换行 / 行数、描边 / 背景、阅读停留、动效；明确输出分辨率、原片裁切 / 缩放和文字与画面的关系。
3. **Sound & Music Specification**：confirmed music mode、sound thesis、原声 / 环境音 / BGM / 旁白政策；每段 preserve / isolate / attenuate / replace / remove / designed_silence 决定，源或 derived asset、成片放置、gain / fade / duck / normalize、完整对白保护与分离失败回退；没有配乐需求时不默认添加。
4. **Transition Specification**：每个接点采用什么及帧数；黑场 / card / hold 若增时，要计入事件与总长。
5. **Mockup 展示与视觉确认 / visual-confirmation.json**：用随附真实关键帧、实际文字和目标输出画幅做一两个可打开的完整画面样稿（含实际采用的相片页 / 录像框等版式），展示给用户；附字体、字号、颜色、位置 / 边距、裁切 / 框体参数与可复用生成入口。确认记录包含 decision_id、状态、确认人 / 时间 / 指令来源、reference 参数指纹、输出规格；每张图列 image_ref / image_digest、source_frame_id / source_image_digest 与应用范围。不逐镜头配对；缺图或未确认保持 proposed，先交草案，禁止正式渲染。视觉可与整包同轮确认，但必须单列。样稿、原图、参数或输出规格变更后，更新对应确认；重算指纹不算确认。
6. **Asset / Constraints**：可读素材、证据、关键帧、字体和参考资源；允许调整、禁改项、status / reason / impact / downstream_handling。封面等仅在本任务要求时提供，其余记 not_applicable。
7. **QA Criteria**：内容、保护范围、时间、文字可读性、音轨 / 接点与 Reference Compliance（成片与 mockup 风格匹配即可，不要求逐帧或逐像素对应）。静态检查和真实播放分开，未实看写 not_tested。
8. **完整执行包确认与机器授权**：单独列出最终取舍、顺序、逐字文字、声音、总时长和允许调整，记录本轮或既有明确确认来源。execution-authorization.json 保存范围、顺序、证据与声音 / 视觉 / 音乐资产指纹；草稿不自动升为 confirmed。已有确认不重复询问；未确认只暂停依赖动作。正式渲染须同时通过声音、视觉、整包与原证据门槛。

机器记录随包携带，接收环境不依赖安装目录：`music-direction.json` 使用 decision_id、status、proposed_mode、recommendation_reason、basis_refs、protected_event_ids、music_flexible_event_ids、confirmed_mode、sound_form、dialogue_separation、separation_fallback、confirmed_by、confirmed_at、confirmation_source。sound_form 枚举 source_mix / original_voice_only / add_music / replace_music / designed_silence；dialogue_separation 为 not_needed / required。采用音乐另列 music_asset_ref、music_asset_digest 与 music_selection（title / version / source / start_ms / end_ms），以及 music_map_required / music_map_ref。

`visual-confirmation.json` 的 output 使用 width / height / fps_num / fps_den；mockups 为数组，每行使用 mockup_id、image_ref、image_digest、source_frame_id、source_image_digest、application_scope。image_digest 与 source_image_digest 为对应文件字节 SHA-256，execution_reference_digest 为同版 reference 文件指纹。status 为 draft / proposed / confirmed；只有明确确认后填写 confirmed_by / confirmed_at / confirmation_source。模板占位、合成示例和已生成的文件不能充当用户确认。

如需 Music Map，随包携带其模板及实际数据：音乐文件引用与全时长、analysis_method、analysis_status、节拍 / 强音毫秒数组、sections / phrases 区间（anchor_id / start_ms / end_ms / label）、av_mapping（event_id / music_ms / sync_tolerance_ms / relationship / reason）及 qa（analysis_verified / notes）。relationship 为 picture_to_music / music_to_picture / intentional_non_sync；保护节点不得为卡点让位。最终地图须有与采用区间相交的实际锚点及核对记录，不能仅写 complete。

时间继续以 source_id + source ms 定位，文字 / 音轨放置优先使用 event anchor + local frames；正式成片坐标按现有时间轴编译对账。异常可以随包继续推进可做部分，但不能豁免证据、完整对白、Edit Boundary、源许可或正式渲染条件。

## Execute 接手入口

接收 Source Clips + Detail Structure + execution-plan + execution-reference + Constraints 组成的完整包。按已确认方案和允许调整制作；不重新选择核心主题、取舍或风格。资源 / 参数仍有缺口时先明确处理，不擅自补造确认结果。
