# 数据契约

目录：文件清单、共同约定、证据记录、场景与片段、Content Map 与外部 Direct、计划映射、剪辑时间轴、静态校验。

## 文件清单

按阶段创建需要的文件。还没到某阶段时允许文件不存在，不用空文件冒充已处理。每个项目放在独立目录。

| 文件 | 格式与用途 |
|---|---|
| project.json | 对象；任务范围、约束、参数、交付目标、版本 |
| capability-map.json | 数组；内部能力和真实工具的映射 |
| sources.json | 数组；源文件、版本、时长、时间映射 |
| frames.jsonl | 每行一个抽样帧证据记录；包含图片定位和机器可追溯 facts / unknowns |
| frame-observations.csv | Broad Structure 的人可读逐抽样帧结构化观察表；供人工 / Director / 其他 Skill 浏览 |
| transcript.jsonl | 每行一条字幕或转写；保留核听状态 |
| scenes.jsonl | 每行一个事件或场景；链接多个源区间 |
| units.jsonl | 每行一个可用的连续片段及其保护范围 |
| reviews.jsonl | 每行一次实际观察的区间、模态、结果与审阅者 |
| deep-observations.csv | Directed Deep Structure 的核心区域高密度观察表；包含完整画面、内容、背景、前后状态、原声、反证及 plan 关系 |
| coverage.json | 数组；按素材、区间、模态记录覆盖状态 |
| overview.md | 带 scene_id 的 source-order 全片导航，不替代证据 |
| content-map.md | 第一轮 Structure 的横向内容地图；链接 scene / evidence / coverage，供人或 Director 做创意判断 |
| brief.md | 可选输入；主题、核心表达、范围、重点和禁改项，可来自用户或外部 Direct |
| editorial-plan.md | 外部 Direct 的 rough plan；记录段落功能、希望寻找的内容、已知线索和待核实判断 |
| candidates.json | 兼容性结构；记录 editorial plan 的映射分支、证据、片段顺序、反例和状态，不要求由本 Skill 自动生成 |
| timeline.json | 对象；主视频轨、音轨、文字轨、输出参数 |
| transitions.json | 数组；每个相邻主视频段落的接续关系 |
| render-manifest.json | 对象；编译后的成片帧轴、接点、轨道坐标、分层缓存键 |
| render-audit.json | 对象；真实导出文件的完整解码计数、时长、近静音及接点图表记录 |
| edit-plan.md | 人可读执行稿，与时间轴保持一致 |
| qa.json | 对象；每项检查、证据、问题及待验证事项 |
| handoff.md | 下一模型从哪里接手、读哪些文件、还差什么 |
| jobs.jsonl | 工具调用、缓存键、状态、产物与可重试错误 |

## 共同约定

- 新建配置及渲染清单的 schema_version 使用 1.1；原有1.0证据记录保留，不为升级重写内容。UTF-8；JSONL 每行独立合法 JSON；未知值用 null，不用猜测值占位。
- source_id、frame_id、utterance_id、scene_id、unit_id、candidate_id、event_id、review_id 各自全项目唯一；一旦被引用不重新编号。
- 所有源区间使用整数 start_ms、end_ms，左闭右开，即包含开始、不包含结束。必须满足 0 ≤ start_ms < end_ms ≤ source.duration_ms。单帧用 timestamp_ms，必须小于 duration_ms。
- 原始文件发生内容变化时建立新 source_id；原版本 ID 保留。只移动位置可更新 locator，保持 source_id 不变。
- evidence_refs 使用带类型的引用，例如 frame:F001、utterance:T001、review:R001。外部前情使用 context_refs，记录来源与核实状态，不伪造本项目证据 ID。
- facts、interpretations、unknowns 分开。facts 中也保留证据来源，区分模型实际观察、用户提供和上游工具输出。
- 第一轮 Broad Structure 与第二轮 Directed Deep Structure 使用同一套稳定 source / scene / unit / evidence ID；第二轮补密时优先更新 verification、context_ranges、protected_ranges 和 review_refs，不复制一个看似全新的平行素材库。
- `frame-observations.csv`、`deep-observations.csv`、`content-map.md`、`brief.md`、`editorial-plan.md` 都是人可读工作层，不替代 JSON / JSONL 原始证据。任何创意判断进入 Execute 前仍须链接回 frame / utterance / scene / unit / review / source range。
- 不把取样帧序号当成源视频帧号。display_timecode 只用于阅读，机器使用毫秒或输出帧号。

## 素材和证据记录

sources 每条必填 source_id、locator、version、duration_ms。version 可以是可核查版本标识或哈希；未知为 null，并阻止复用旧缓存到精确剪辑。其他字段包括 episode、width、height、fps_num、fps_den、frame_rate_mode、audio_streams、subtitle_source、time_mapping。

frame 必填 frame_id、source_id、timestamp_ms、image_ref、facts、unknowns。建议补充 sheet_id、cell_index、visible_text、observation_origin。cell_index 为一至九，不参与时间计算。frame 只描述该时点看见的状态。

`frame-observations.csv` 是同一批抽样帧的**人可读结构化层**，不是另起一套证据 ID。每行对应一个已实际分析的 sampled frame，推荐字段：`source_id`、`episode`、`timestamp_ms`、`display_timecode`、`frame_id`、`sheet_id`、`cell_index`、`scene_id`、`characters`、`visual_facts`、`visible_action_state`、`expression_gaze`、`spatial_relationship`、`setting_background`、`key_objects`、`visible_text`、`nearby_dialogue_refs`、`content_description`、`interpretations`、`unknowns`、`evidence_ref`、`image_ref`、`coverage_status`。

其中 `visual_facts` / `content_description` 不得把相邻抽样帧之间未实际观察到的动作补齐；`interpretations` 必须与事实分列。这里的“逐帧”始终指逐**已分析抽样帧**。

utterance 必填 utterance_id、source_id、start_ms、end_ms、text、origin、audio_verified。origin 为 subtitle、asr、manual 或 user；audio_verified 默认为 false。其他字段包括 speaker、addressee、language、translation、unclear_words、review_refs。未知说话人保持 null，不能按画面中出现的人直接指定。

review 必填 review_id、source_id、start_ms、end_ms、modalities、reviewer、result、evidence_locator。modalities 是实际处理的 video、audio、frames 或 text 列表；reviewer 说明来自模型、工具或用户。保留能复核的工具输出、人工确认记录或音画位置。只有提取音轨的日志不算 audio 审阅。

coverage 每条包含 source_id、start_ms、end_ms、modality、method、status、evidence_file、reason。modality 为 visual_sample、transcript 或 av_review；status 为 complete、partial、failed、pending、excluded。complete 只指该模态在该区间按所列方法处理完成。excluded 必须有理由。覆盖率按区间并集计算，不把批次重叠重复计入；不能把 visual_sample 的完成率叫作完整观看率。

## 场景和片段

scene 包含 scene_id、source_ranges、characters、location、story_time、facts、interpretations、unknowns、before_state、after_state、evidence_refs、context_refs。source_ranges 是若干 source_id/start_ms/end_ms 对象，允许交叉叙事。story_time 不确定时写 null。

unit 包含以下字段。一个 unit 只能对应一个源文件中的连续区间。

```json
{
  "unit_id": "U001",
  "scene_id": "S001",
  "source_id": "SRC001",
  "start_ms": 120000,
  "end_ms": 145000,
  "context_ranges": [{"source_id":"SRC001","start_ms":100000,"end_ms":170000}],
  "protected_ranges": [{"start_ms":122000,"end_ms":142000,"reason":"完整问答与动作回应"}],
  "summary": "示例占位，须据实际素材填写",
  "utterance_ids": ["T001"],
  "evidence_refs": ["utterance:T001"],
  "visual_state": {"costume":null,"props":null,"position":null,"lighting":null},
  "relationship_stage": null,
  "audio_state": {"speech":true,"music":null,"ambience":null},
  "isolated_use_risk": "缺少前一问时指代不清",
  "verification": {"audio":"pending","visual":"pending","context":"pending","review_refs":[]},
  "unknowns": ["尚未回看连续音画"]
}
```

verification 的 audio、visual、context 使用 pending、reviewed、not_applicable。not_applicable 在 not_applicable_reasons 对象中按对应字段说明原因，例如已确认源文件完全没有音轨。仅仅没有对白不等于音频不需检查。reviewed 必须有 review_refs，值为 reviews.jsonl 中真实存在的 review_id；不能仅靠摘要设置。连续画面核查使用 video 模态，仅有 frames 不能标记 visual=reviewed。核查区间合计应覆盖实际选用的片段。protected_ranges 可以在探索期暂为空，精查后入选执行稿时必须有明确保护范围，或在 protection_note 写明为何整段无可保护的对白、动作且经复核。

## Directed Deep Structure 的结构化观察

`deep-observations.csv` 用于第二轮定向高密度 Structure。它不是剪辑表的替代品，也不能只记录“可用 / 不可用”。当某个区域已经被 rough plan 选为核心回查对象时，应先把它做成更完整的内容档案，再收敛为 unit 和切点。

推荐每行对应一个高密度观察时点或连续观察区间，字段至少包括：

- 定位：`observation_id`、`plan_node_id`、`source_id`、`episode`、`start_ms`、`end_ms`、`display_range`、`scene_id`、`unit_id`、`representative_frame_refs`；
- 画面：`visual_facts`、`shot_composition`、`action_chain`、`expression_gaze`、`spatial_relationship`；
- 背景：`setting_context`、`narrative_context`；
- 内容：`content_description`、`dialogue_audio`、`before_state`、`after_state`；
- 判断：`interpretations`、`unknowns`、`evidence_status`、`counterevidence`；
- 执行衔接：`context_ranges`、`protected_ranges`、`isolated_use_risk`、`review_refs`、`narrative_function`、`edit_note`。

字段含义：

- `visual_facts` 写这一时段实际看到的画面；人物、站位 / 朝向、动作、表情 / 视线、人物间距离、物件、景别 / 构图与明显画面变化尽量具体；
- `content_description` 回答“这一小段实际发生了什么”，不只抄对白；
- `setting_context` 写地点、时间、环境、空间状态等场景背景；
- `narrative_context` 写它在完整事件中的位置、前一事件和后续关系；
- `dialogue_audio` 写已核听的原声信息，并明确 speaker / addressee / tone / pause / ambience / music / audio_verified；
- `before_state` / `after_state` 用于保住动作与因果，不等同心理推断；
- `plan_node_id` / `narrative_function` 只说明为什么要回查这一段，不得用计划目标倒推事实；
- `evidence_status` 可用 pending、supported、contradicted、partial；关键节点若为 contradicted 或仍 pending，不进入 ready_for_render。

第二轮可以在第一轮相同 frame_id / scene_id 上补充更密的新 frame / review，也可以对连续区间形成新的 observation_id；不要为了“更细”而复制一套与第一轮断开的素材库。

## Content Map 与外部 Direct

`overview.md` 和 `content-map.md` 作用不同：

- `overview.md` 按源时间顺序帮助恢复“原片发生了什么”；
- `content-map.md` 横向组织人物、关系变化、重复行为、对白主题、无声互动、物件 / 空间线索、潜在前后呼应与 unknowns，帮助人或 Director 看见“素材里都有什么可以继续想”。

Content Map 中每个可操作条目应尽量带 `scene_id`，必要时补 source range / evidence refs / coverage 状态。它可以写“可能形成对照”“值得进一步回看”等导航性解释，但必须与事实分开，不能把尚未连续核实的推测写成已成立主线。

`brief.md` 与 `editorial-plan.md` 属于 Direct 层输入。它们可以在仓库外形成，也可以复制 assets 模板。对核心执行而言：

- Brief 说明要表达什么、范围、重点和约束；
- Rough Editorial Plan 说明准备怎样组织观看关系、每段承担什么功能、希望回原片寻找什么；
- 它们不要求预先精确到帧，也不因写得详细就自动升级为素材事实。

Directed Deep Structure 要把 rough plan 的每个核心节点映射回已有 Content Map 与原片。建议维护一个 plan mapping 表，至少包含：`plan_node_id`、`function`、`scene_refs`、`unit_refs`、`evidence_refs`、`evidence_status`、`gaps`、`counterevidence`、`allowed_adjustment`。该表可放入 `editorial-plan.md` 附录，或以项目自定义 JSON 保存；当前核心脚本不强制固定文件名。

若 evidence_status 仍为 pending / contradicted，不进入 ready_for_render。若关键证据冲突，应返回 Direct 调整 rough plan，而不是由执行层悄悄改成另一条主题。

## 计划映射与 candidates 兼容结构

`candidates.json` 保留用于兼容既有项目和多分支 rough plan。candidate 不再意味着“必须由本 Skill 自动想出的创意主线”；它可以是用户 / Director 提供的 editorial plan 分支，也可以是明确授权 brainstorming 时产生的草案。

candidate 建议包含 candidate_id、origin、thesis、experience、mode、unit_order、roles、claims、counterevidence、unknowns、status。`origin` 可使用 user、director、brainstorming、legacy_auto 等值。mode 为 contrast、payoff、behavior_change 或 perspective；必要时可用自定义值并解释。

claims 每条至少含 text、evidence_refs、status。status 为 supported、interpretation 或 pending；有证据并不自动等于某种心理动机得到证明。counterevidence 记录可能改变主线的上下文；尚未查找时写 pending，不留空后声称不存在。

candidate.status 为 provisional、ready_for_plan 或 rejected。ready_for_plan 表示 rough plan 对应的核心素材已经完成 Directed Deep Structure、语境和反证已经检查，不表示粗剪通过。补充 estimated_duration_ms、scope_changes、reorder_reason 和 selected 字段方便执行。

## 剪辑时间轴

timeline 顶层包括 schema_version、project_id、candidate_id、status、coordinate_space、fps_num、fps_den、width、height、events、audio_tracks、text_tracks。status 为 draft 或 ready_for_render。未确定输出规格时保持 draft，未知数字为 null。1.1版使用 coordinate_space=assembly 保存未扣除叠化的编排计划；实际成片坐标由 render-manifest.json 提供。旧版无叠化时两者重合，仍应在出片前完成编译，避免下游混用。

主视频 events 按 out_in_frame 排序，左闭右开，从零开始无缺口、无重叠。每条包含 event_id、kind、out_in_frame、out_out_frame、function。kind=source 时还需 source_id、unit_id、source_in_ms、source_out_ms、speed。默认 speed=1。kind=card 时记录 card_text 或 card_asset，不借用伪造的 source_id。

每段源素材的播放长度应与输出帧数对应，允许不超过一个输出帧的量化误差；误差不能逐段累计，编译时间轴时以累计时间统一量化。精剪仍需按真实解码结果核对。源可变帧率不影响输出采用确定帧率，但必须记录源到输出的映射。

audio_tracks 每条含 track_id、kind、source_id 或 asset_ref、source_in_ms、source_out_ms、out_in_frame、out_out_frame、gain_db、fade_in_ms、fade_out_ms、sync_event_id、reason。kind 区分 original、music、voiceover、ambience。明确是否保留原声；异步 J/L-cut 要说明语义与同步范围，不能把音轨默认等同主视频切点。未知增益和淡化写 null，核听后确定。编译输入优先使用 anchor_event_id、local_in_frame、local_out_frame，编译器据实际段起点生成 out_in_frame/out_out_frame；对确实跨段的绝对定位须显式 coordinate_space=output，并在结构变动后重核。

text_tracks 每条含 text_id、kind、text、out_in_frame、out_out_frame、position、font、font_size_px、color、motion、evidence_refs。kind 区分原声字幕、解释、场景提示。解释不得伪装原话。像素规格未定时使用相对坐标并标记待定。

文字轨也使用 anchor_event_id/local_in_frame/local_out_frame 编译。补充 stable_hold_frames、fade_in_frames、fade_out_frames、glyph_height_px、font_unit、font_size_value、anchor_reference，记录阅读时间和字号校准。fade_in+stable_hold+fade_out 不得超过显示范围；章节卡延长会修改事件长度，不能只修改文字轨。原音不许含音乐等要求写入 project.audio_policy，音频修复必须遵守。

转场使用 transitions 中独立记录；timeline 中各段保持未扣叠化的顺序区间。transition 新增 effect=hard_cut/xfade 与 overlap_frames；硬切为0，叠化为正整数。编译后各段在 render-manifest 中允许按明确的 overlap_frames 相邻重叠，并生成每个接点的成片开始、结束帧。须核查源边界和 protected_ranges；不能把两个片段的完整长度相加后又偷偷扣除叠化时间。双时间轴、量化方法及所有下游坐标更新规则见“渲染与工程检查”。

transition 必填 from_event、to_event、relation、reason、omitted_context、audio_method、time_cue、risk、review_status。relation 使用重组规则规定的五个值。review_status 为 pending 或 reviewed；有几个接点就检查几个，不能只抽查一个代表全部。

render-manifest 顶层记录 coordinate_space=output、fps_num/fps_den、total_frames、duration_seconds、events、joins、audio_tracks、text_tracks、cache_keys、warnings、input_digest。event 同时保留源取段与最终输出帧号；joins 包含 start_frame/end_frame，硬切两者相同。封面从成片选取时引用此坐标；从源片选取时仍记录 source_id 与源时间，不混称同一坐标。

cache_keys 分开标识视频单元、无字合成、音频混音和文字成片层。render-audit 记录 file_sha256 与 manifest_sha256，以确认审查的是同一个版本。expected_quiet_ranges 使用成片 start_frame/end_frame 与 reason，供人工解释有意静默；未提供理由不能自动豁免。

人可读执行稿表头统一为：成片时间及帧号｜原素材及时间码｜画面与动作｜原声及音轨｜屏幕文字｜字号位置｜接续与注意事项。另附素材取舍表、完整文字清单、封面选帧和 EVA。

## 静态校验

随附脚本检查 sources、frames、transcript、reviews、units、timeline 的核心 ID、源范围、保护区间、帧时长，以及 transitions 的相邻引用。ready_for_render 还检查核查记录的存在及音视频区间覆盖。它不会证明核查记录所写事实真实、说话人正确、剧情因果成立、实际音画流畅或字幕准确。JSON 合法也不等于数据契约所有语义要求得到满足。

运行 `python3 scripts/validate_project.py 项目目录`；缺失后续阶段文件列为 skipped，不得把输出 status=pass 解释为项目已完成。进入 ready_for_render 前仍须按检查与交接规范人工或模型复核全部相关字段。
