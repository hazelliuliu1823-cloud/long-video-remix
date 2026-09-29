---
name: long-video-remix
description: 从三到五小时或多集影视、活动视频中建立可回查的画面与原声索引，形成可检索 Content Map；在人工或独立编导流程给出 brief / rough editorial plan 后，重新回到原素材做定向高密度核验，并把方案落实为可执行剪辑时间轴、渲染清单与成片核查。用于长视频结构化、九宫格分析、逐抽样帧记录、定向精查、同集重组、跨场景主题混剪、剪辑执行稿、分层渲染、成片返工、导出核查及跨模型交接；不把通用创意选题与完整编导策划作为默认职责。
---

# 长视频结构化与混剪执行

公开仓库版本 v1.0.1 · 2026年9月29日

本 Skill 的核心不是“一句话自动生成成片”，而是把长素材先整理成有来源、可检索、可回查的内容空间，再把人工或独立编导形成的 rough plan 可靠地压回原素材证据，并落实成真正可执行的剪辑方案。

整体工作分为三个功能层：

- **Structure**：先广覆盖建立 Content Map；有了 rough plan 后，再回原片做第二轮定向高密度 Structure。
- **Direct**：决定“值得讲什么、为什么这样讲、怎样形成观看关系”。这一层默认由人、brainstorming 或独立 Director 流程完成。
- **Execute**：把已确定的方向与已核实素材编译成时间轴、渲染清单、粗剪 / 成片及 QA。

Structure 不是只做一次。标准路径是：

```text
Source
  ↓
Broad Structure
  ↓
Content Map
  ↓
Human / Director：Brief + Rough Editorial Plan
  ↓
Directed Deep Structure
  ↺ 证据不足时返回 Direct 调整
  ↓
Execute
```

抽帧负责发现，连续音画负责核实，完整片段负责剪辑。允许改变叙述顺序和集中呈现分散线索；保留原话含义、真实指向、必要因果和动作完整性。

## 执行边界

- 按本轮明确要求、已确认方案、指定素材、一般默认值的顺序执行。未经要求，不改原 Handoff、已有成片或已确认的编导主线。
- 先核查可用模型及工具，按能力映射 MCP；本 Skill 中的能力名均为内部抽象名，不是真实工具名。没有调用成功记录，不写成已经完成。
- 默认以角色和剧情为对象。公开活动只描述可见行为和观看感受，不由混剪推断真人私下关系、性取向或心理。
- 不凭抽样帧补出未见动作，不凭转写补出未听台词，不把用户摘要或工具标签改写为亲眼观察。
- **Broad Structure 不因已有 brief 过早缩窄覆盖。** brief 可以帮助标注重点，但第一轮仍要保留整体内容面、coverage 和 unknowns。
- **Rough Editorial Plan 是创意意图，不等于素材已经证明。** 第二轮 Directed Deep Structure 必须重新回到相关原片核对。
- 如果第二轮证据与 rough plan 冲突，报告冲突、替代素材和缺口；默认不通过剪辑技巧强行证明原方案，也不擅自改写已确认的核心表达。
- 同一集优先；同一事件、对白指向和关系阶段优先级高于服装相似。跨集须有明确主题联系，并让观众辨认时空变化。
- 删段不删句，删重复不删因果。必要问答、否定、条件、迟疑、回应和动作后果共同决定最短保留范围。
- 默认不改写原声、不拼接词语制造新对白、不借用异场反应冒充即时回应。明确要求架空或恶搞时另行约定，不沿用剧情准确混剪的事实标签。
- 不强制每条五至八段或四十五至六十秒。未给时长时先提出由证据支持的时长，再试剪；不为达到配额拆碎互动。
- 不设固定审批关卡。有明确授权就继续；仅在素材缺失、关键意思不确定或需扩大用户明确限定范围时，完成可做部分后提出一个具体问题。

## 开始工作

1. 读取 [工作流程](references/workflow.md) 和 [数据契约](references/data-contracts.md)，建立任务目录与 `project.json`。
2. 读取 [MCP 适配](references/mcp-adapter.md)，发现真实能力、记录映射并完成小范围探测。只使用获授权的素材访问与处理范围。
3. 检查已有产物。按源文件版本和配置恢复进度；不因切换模型重复扫描完整视频。
4. 如果当前任务只要求 Structure，可在 Content Map 完成后正式交付，不必进入 Direct 或 Execute。
5. 如果要继续混剪，读取已有 brief / editorial plan。没有时，先把 Content Map 交给用户、brainstorming 或 Director 流程形成 rough plan；本 Skill 不默认越过这一层自行决定创意主线。
6. 从当前可验证阶段开始，按下面的顺序推进。缺少某种观察能力时降级输出，并明确标签。

## 工作顺序

| 阶段 | 执行动作 | 产物 | 进入下一步的条件 |
|---|---|---|---|
| A 素材登记 | 确认版本、时长、时间基准、字幕匹配、能力与配置 | project、sources、capability-map | 能把后续证据定位回原素材；否则只做准备 |
| B Broad Structure | 全时段粗扫画面和台词；逐张记录已分析抽样帧的结构化观察，保留无声段及未覆盖区域 | frames、frame-observations、transcript、coverage | 可识别覆盖与缺口；人工 / Director 不必重新从九宫格猜内容 |
| C Content Map | 在逐抽样帧观察之上合并镜头为事件，建立 scene / 初步 unit、source-order overview 和跨场景内容地图 | scenes、units、overview、content-map | 形成足够完整且可下钻回 frame observation 的素材面；若 deliverable=content_map 可在此正式交付 |
| D Editorial Plan Intake | 接入由人 / brainstorming / Director 形成的 brief 与 rough editorial plan，明确已确认主线、段落功能、重点线索和禁改项 | brief、editorial-plan、plan mapping | 创意方向足以指导定向深挖；不要求已有精确切点 |
| E Directed Deep Structure | 带着 rough plan 回到相关原素材，提高抽样 / 播放密度；先补完整画面、内容、背景、前后状态与原声，再做剪辑判断 | deep-observations、已核实 units、reviews、protected_ranges、evidence gaps | 每个核心节点有足够音画、内容与语境证据；不成立时退回 D 调整 |
| F Execute | 校准文字；编译叠化后的时间轴；分层渲染；生成全接点图表 | timeline、transitions、render-manifest、edit-plan、rough-cut | 实测帧数与时长；近静音窗口有记录，再继续音画实看 |
| G QA & Handoff | 逐接点及全片复核，做 EVA，保存问题与缓存版本 | render-audit、接点图表、qa、handoff | 技术检查与人工观看分别记录，不以成功日志代替验收 |

## Structure 的两种密度

### 第一轮：Broad Structure

目标是**扩大可见范围**，不是提前替某个选题找证明。

- 全时段建立基础画面与台词覆盖；
- 对每张**已实际分析的抽样帧**建立结构化观察：可见人物、动作 / 状态、表情 / 视线、空间关系、环境背景、物件、可见文字、邻近对白、内容说明、interpretations 与 unknowns；
- 同时保留机器可追溯的 `frames.jsonl` 与便于人工 / Director / 其他 Skill 阅读的 `frame-observations.csv`；
- 场景、人物、事件、关系变化和无声互动都保留入口；
- 形成 source-order overview 和跨场景 Content Map；
- 明确抽样、字幕 / ASR、连续音画核实三种 coverage 的差别；
- 不把未处理区域悄悄排除。

### 第二轮：Directed Deep Structure

目标是**把 rough plan 重新压回原片证据**。

- 根据计划节点提高抽样密度或直接连续播放；
- 先建立 `deep-observations.csv`：完整记录人物与站位、镜头 / 构图、动作链、表情 / 视线、空间关系、场景环境、关键物件和画面变化；
- 写清这一核心区域**实际发生了什么**，并补充 setting_context、narrative_context、before_state、after_state；
- 从台词命中扩展到完整问答、动作链和必要前后文，核听说话人、对象、语气、否定、条件、停顿、环境声 / 音乐和动作后果；
- facts、interpretations、unknowns 分开，检查反证、误读风险和时空关系；
- 在完整理解之后，再把初步 unit 收敛为可剪 unit，并形成 context_ranges、protected_ranges 与 isolated_use_risk；
- 如果原计划不成立，把具体问题返回 Direct，而不是直接替用户重写核心创意。

## 决策时读取

- 抽帧密度、批次、Content Map、第二轮定向回查和恢复：读取 [工作流程](references/workflow.md)。
- 时间码、记录字段、Content Map / editorial plan 关系和时间轴：读取 [数据契约](references/data-contracts.md)。
- 换模型或 MCP、能力缺失、调用失败：读取 [MCP 适配](references/mcp-adapter.md)。
- 在既定 rough plan 下保住完整对白、连续性与正确重组关系：读取 [重组与剪辑规则](references/montage-rules.md)。
- 首次出片或返工：读取 [渲染与工程检查](references/render-engineering.md)，按文字校准、时间轴编译、分层渲染、解码实测、全接点检查顺序执行。
- 交付前、移交另一模型：读取 [检查与交接](references/qa-handoff.md)。
- 需要演示两轮 Structure、外部 Direct 和 Execute 的衔接：读取 [执行示例](references/worked-example.md)。示例均为虚构，不是当前素材。

复制 `assets/project-template.json` 建立配置。Broad Structure 可复制 `assets/frame-observation-template.csv` 建立人可读逐抽样帧观察表；第二轮可复制 `assets/deep-observation-template.csv` 建立核心区域高密度观察表。需要 Direct 时，可复制 `assets/brief-template.md` 和 `assets/editorial-plan-template.md`，也可以直接接入用户已有的编导文档。复制 `assets/timeline-template.json` 建立时间轴。

具备 Python 时运行 `scripts/validate_project.py 项目目录` 检查来源、时间和引用；不具备 Python 时按数据契约逐项核查，并写明为人工或模型静态检查。脚本不判断剧情真伪或观看流畅度。

进入实际渲染时，用 `scripts/compile_render_manifest.py 项目目录` 编译成片坐标与缓存键，再按 [渲染与工程检查](references/render-engineering.md) 使用 `scripts/audit_render.py` 实测导出并生成接点对照表。前者需要 Python；后者需要 Python 和 FFmpeg，拼图额外需要 Pillow。缺少能力就列明未验证项，不填通过。

## 每次工作结束

先交付已完成产物，再用短文字说明：本次处理范围、当前处于 Broad Structure / Direct / Directed Deep Structure / Execute 的哪一层、发现、未验证项和下一步。更新 `handoff.md` 及 `coverage.json`。同一项目保留稳定 ID；修订增加版本，不能让旧引用悄悄指向不同素材。不要以再次询问已确认事项代替推进。
