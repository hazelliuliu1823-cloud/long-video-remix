# 工作流程

## 总体路径

本流程不是单向的“结构化 → 自动选题 → 剪辑”。标准路径是：

```text
A 素材登记
  ↓
B Broad Structure：全量粗覆盖
  ↓
C Content Map：把长素材变成可检索的内容面
  ↓
D Editorial Plan Intake：人 / brainstorming / Director 形成 brief + rough plan
  ↓
E Directed Deep Structure：带着 plan 回原片做高密度补查
  ↺ 证据不足 / 计划不成立时返回 D
  ↓
F Execute：时间轴与渲染
  ↓
G QA & Handoff
```

第一次 Structure 追求**广度**，第二次 Structure 追求**与 rough plan 相关的深度**。不要在第一轮为某个主题过早押题，也不要在第二轮仅凭第一轮摘要直接精剪。

## 任务与默认值

接收视频文件或授权地址、已有九宫格、字幕、转写和分析文档。优先复用已完成工作，但先核对它们对应的源视频版本与时间轴。用户只提供九宫格时可以建画面索引，不能据此交付已核实的对白剪辑。

配置必须写明：素材范围、目标人物（如有）、已知目标或开放 Structure、是否限同集、成片比例和时长、原声与配乐要求、已有底稿、交付目标、可用工具。未知项写 null；对不影响前期建档的缺项先继续工作。无指定时，以同集为优先、保留原声、只用必要解释文字；时长和比例不擅自写成用户已确认要求。

`deliverable=content_map` 时，默认目标是完成 A—C 并正式交付 Content Map。`deliverable=detailed_plan` 或更后续产物时，必须在进入 E 前取得 brief / editorial plan；它们可以来自用户、人工编导、brainstorming 或独立 Director 流程。

已有 brief 可以在 Broad Structure 阶段作为重点标记，但不得让第一轮覆盖只剩关键词检索。Structure 的价值之一就是扩大人的可见范围，让后续 Direct 不被最初假设锁死。

默认不主动渲染。只有明确要求或任务已包含试剪时才调用渲染；下载、上传、付费和访问私有资源均受当前环境授权约束。不得发布、发给他人或覆盖源视频。

## A 素材登记

为每个源文件建立 source_id，记录文件位置、可取得的版本标识或哈希、时长、流起点、分辨率、帧率信息、是否可变帧率、音轨和字幕。拿不到元数据时标记未知，不从文件名推断集数或版本。

项目时间基准采用原文件从首个展示时刻起算的非负毫秒；保留容器原始 PTS 与项目时间的映射。合集切出单集、代理文件、音轨分块都记录原片偏移。若转换并非线性偏移，保存完整映射，不能直接套加法。

字幕先抽查开头、中段、末段与原声的对应。不同版本可能出现片头长度差、删减或累计漂移；只有验证为恒定偏移时才能整体平移。候选段字幕必须局部复核。无法听音时只能记“未核对”。

## B Broad Structure：全片概览

画面和台词分别扫描，再按同一时间轴合并。不要只按台词关键词找候选，否则会漏掉等待、递东西、回望等无声互动。

下表是第一轮可调试的参数，不是质量保证或平台限制。

| 参数 | 起始建议 | 调整条件 |
|---|---|---|
| 分析批次 | 以场景为主，必要时每五至十分钟分批 | 依据图片数、分辨率、上下文和服务时长限制缩小 |
| 批次边缘 | 先取前后各十五至三十秒辅助语境 | 一轮对话仍跨界时继续扩展到事件边界 |
| 概览抽帧 | 镜头代表帧加长镜头约五至十秒补帧 | 快动作、遮挡、无声互动或不确定处增加 |
| 第二轮精查抽帧 | 候选相关段可从每秒一至两张开始 | 动作起止用连续播放或更密抽帧核实 |

九宫格是展示方式，不等于分析时间单位。每格保留 frame_id、source_id、真实取帧时间；从左至右、从上至下按时间排序。跨场景清楚标记。保留原分辨率单帧；文字或表情看不清就读取单帧或放大，不能凭缩略图补写。

每张已分析抽样帧都要留下两层记录：

1. `frames.jsonl`：机器可追溯证据，保留 frame_id、真实时间、image_ref、facts、unknowns；
2. `frame-observations.csv`：面向人工 / Director / 其他 Skill 的结构化观察表。除定位外，至少覆盖 characters、visual_facts、visible_action_state、expression_gaze、spatial_relationship、setting_background、key_objects、visible_text、nearby_dialogue_refs、content_description、interpretations、unknowns。可复制 `assets/frame-observation-template.csv`。

这张表不是九宫格的重复说明，而是把“每一张已看过的抽样帧里真正有什么”变成人可浏览的中间层。相邻帧间的动作只能作为待核实假设。请求“逐帧文档”时说明这里是逐抽样帧记录，并列抽样规则，不声称看过每个视频帧。

机器检测的镜头切换先作为技术边界。同一轮正反打通常仍属于一个场景；闪白、运镜和灯光变化可能需要人工复核。保留检测原结果及调整结果，不用算法切点直接决定叙事单元。

coverage 分别记录画面抽样、字幕或转写、连续音画复核的时间区间与状态。全时段完成抽样不等于全时段实看。任何未处理、失败或低清区域都保持可见；特别记录片头片尾是否有正片内容。

Broad Structure 的完成条件不是“已经知道该剪什么”，而是：素材主要时间范围已经建立基础索引，场景和对白可以回查，coverage 与 unknowns 清楚，人或 Director 有足够完整的素材面继续判断。

## C Content Map：场景理解与结构化输出

先写场景事实：人物、地点、可确认的剧情时间、进入时的状态、动作与对白、离开时的状态。再写解读与候选价值。场景可以覆盖多个不连续镜头；交叉叙事需记录多个源区间，不假装它们是一个连续事件。

将跨批次同一对话合并。用 source_id、区间和证据 ID 去重；不要因重叠读取把同一个动作算成发生两次。

`overview.md` 保留 source-order 导航：事件顺序、关系变化、重复线索、未确认事项，每一项链接 scene_id。它不能替代台词原文、`frames.jsonl`、`frame-observations.csv` 和场景卡。Content Map 中的重要线索应能继续下钻回 scene，再下钻到具体 frame / utterance / review，而不是只剩摘要。

同时生成 `content-map.md`。它面向后续人工 / Director，不按源时间顺序机械罗列，而是在不丢证据链接的前提下提供可横向浏览的素材面，例如：

- 人物 / 关系及其变化节点；
- 重要事件和重复出现的行为；
- 可检索对白主题和原声位置；
- 无声互动、物件、空间和动作线索；
- 前后呼应、潜在对照、尚未确认的关联；
- 每项对应 scene_id / source range / evidence refs；
- coverage 缺口和 unknowns。

Content Map 可以提示“这里可能值得继续看”，但不把这种提示写成已经确认的编导结论。

建立初步 unit。每个 unit 必须是同一源文件中的连续区间；若跨源或不连续，拆成多个 unit 并用 scene_id 或后续 plan_id 关联。第一轮 unit 可以较粗，记录可取范围和回查语境范围；`protected_ranges` 可以等待第二轮核验后补齐。unit 没有固定秒数。

如果 `deliverable=content_map`，A—C 完成后就是合法终点。交付时明确哪些内容来自抽样、字幕 / ASR 或连续音画实看，不为了进入后续流程强行生成创意主线。

## D Editorial Plan Intake：接入外部 Direct

Direct 是创意层。默认由人、brainstorming、独立 Director Agent 或用户现有方法完成。本 Skill 在这一阶段主要做**接入、澄清结构和建立回查目标**，不是重新替用户自由选题。

最小输入可以只是一份自然语言 brief；更推荐提供 rough editorial plan。可使用 `assets/brief-template.md` 和 `assets/editorial-plan-template.md`，也可以直接接入已有文档。

rough plan 至少应让后续系统知道：

- 核心表达或观看关系；
- 各段落大致承担什么功能；
- 希望寻找哪些事件 / 对白 / 动作；
- 哪些素材线索已经知道；
- 哪些判断必须保留、哪些可以调整；
- 哪些节点目前只是推测，需要第二轮回原片确认。

不要求 rough plan 预先给出精确时间码。若它已经包含时间码，也只能当作定位线索，仍要按源版本和实际音画重新核验。

把 rough plan 映射到 Content Map：每个计划节点链接已有 scene / unit / evidence；没有对应项的节点登记为 evidence gap。不要为了让 plan 看起来完整而把弱证据升级为事实。

如果用户明确授权本 Skill 辅助 brainstorming，可以给出基于 Content Map 的建议，但要与后续执行记录分开，并明确这是 Direct 层草案。默认情况下，已确认的核心表达优先，不自行改成另一条主题。

## E Directed Deep Structure：带着计划回原片

这是第二轮 Structure，也是从“rough plan”进入“可剪方案”的关键步骤。

对 editorial plan 中每个节点重新回到原素材，不仅复用第一轮摘要。先读取对应 scene / unit / transcript / frames / frame-observations，再提高信息密度。第二轮的顺序是**先重新把核心区域看完整，再决定怎么剪**：

- 相关片段从前后各十五至三十秒开始扩查；指代、条件、人物动机或动作因果仍不清楚时继续扩到完整事件，必要时追溯前后场景或前集；
- 候选段可从每秒一至两张抽帧开始，但动作起止、反应链、停顿和声音关系必须用连续播放或等价能力确认；
- 建立 `deep-observations.csv`（可复制 `assets/deep-observation-template.csv`），每个核心观察区间至少补齐：
  - **visual_facts**：人物、站位 / 朝向、动作、表情 / 视线、人物距离、关键物件、景别 / 构图、画面变化；
  - **setting_context**：地点、可确认时间、环境与空间状态；
  - **narrative_context**：前一个事件是什么、为什么来到这一刻、它与前后事件怎样连接；
  - **content_description**：这一小段实际发生了什么，不能只复制字幕关键词；
  - **dialogue_audio**：原声对白、说话人、对象、语气、停顿、环境声 / 音乐及核听状态；
  - **before_state / after_state**：进入和离开这一段时人物 / 事件状态；
  - **interpretations / unknowns / counterevidence**：把事实、解读和不确定性分开；
  - **plan_node_id / narrative_function**：这一段为什么被回查、准备承担什么功能，但该字段不能反过来污染事实描述。
- 字幕 / ASR 命中必须回到原声核听；逐一核对说话人、被说话人、否定词、条件、重要停顿、动作发起与回应、动作后果；
- 检查 rough plan 可能忽略的反证、玩笑语境、时间差、关系阶段和异场反应；
- 在上述内容理解完成后，再把第一轮粗 unit 收敛为可剪 unit，确认 context_ranges、protected_ranges、isolated_use_risk 和 verification；
- 为接续关系准备连续性、比较、倒叙、章节变化等依据。

记录审阅者身份或能力来源、时间范围和结果。只有文件实际被读取不等于被看懂；音频抽取成功也不等于原声已核听。不能处理音频或连续视频时，请有能力的工具或用户核查；同时继续可做的索引和草案。

### 何时返回 Direct

以下情况不要直接进入 Execute：

- rough plan 的关键节点在原片中没有足够证据；
- 原台词含有被计划忽略的否定、条件或玩笑语境；
- 计划把不同事件误当成同一问答或即时反应；
- 某个段落功能需要的素材不存在，只能靠强解释文案弥补；
- 新发现的前后文会改变核心表达。

此时输出具体 evidence gap、冲突证据和可替代素材，返回 D 调整。允许多次 D ↔ E 循环。不要因为已经投入精查成本就强行保留原计划。

## F Execute：执行与粗剪

实际出片前读取“渲染与工程检查”。先用锚点和对照帧校准文字，再按实际叠化帧数编译 render-manifest；所有成片文字、音轨放置、封面定位和接点核查使用此版本成片坐标。分开保存视频单元、无字底片、混音和文字烧录产物，便于局部返工。

先生成 edit-plan，再编译 timeline。详细稿包含成片参数、主线、源素材取舍、逐段画面、原声、创作者文字、字号位置、转场、封面、禁止项和待验证项。画面、声音、文字分别设计，同一主句可跨原片正反打保留。

粗剪先保留必要原声及最少的场景提示，验证结构，再加配乐和包装。按照转场逐个观看接点，再正常速度看全片。原片音乐无法干净衔接时优先换切点、加长段落或接受明确场景切换；不假设淡化即可解决所有音乐断裂。

用户只要执行稿时，交付 detailed_plan；未生成粗剪则 rough_cut_verified=false。用户要成片而当前没有渲染能力时，交付能够直接执行的计划与明确缺口，不谎称已剪好。

每次导出先完整解码实测帧数和展示时长，再做全片低电平扫描，并从该成片自动生成全部接点对照图。技术错误先修复；近静音和接点图进入实际核听、播放，不能用截图代替动态检查。

## G QA、保存与恢复

每批成功后保存结果和 coverage；每阶段结束保存 handoff。缓存键由源文件版本、处理区间、参数、工具及模型版本组成。换源版本时重新核对时间码；调整 Broad Structure 抽样密度只重做受影响区间；Direct 调整通常复用第一轮 Content Map 与已验证证据，不重扫全片。

如果 rough plan 改动只影响局部节点，优先只重做对应的 Directed Deep Structure 区域。只有新的方向依赖此前完全未覆盖或低可信区域，才扩展相应 Structure 范围。

切点或片段长度变化，强制失效对应片段及下游缓存；不能只看同名文件是否存在。将片段 manifest、渲染参数及实际时长纳入缓存判定。纯文字改动可复用无字底片和已确认音轨；卡片或转场时长变化则须重新编译并更新所有下游位置。

下一模型先读 handoff、project、capability-map、sources、coverage、content-map 和 editorial plan，再按需读取相关 scene / unit / review / evidence。不得仅凭前一模型的 overview 或 rough plan 把未看部分写成已验证。
