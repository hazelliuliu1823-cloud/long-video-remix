# long-video-remix

> **Make video queryable before you make it editable.**
>
> Turn hours of multimodal footage into compact, searchable structured data — then use that structure for editing, research, content analysis and execution.

`long-video-remix` 的核心不是“让 AI 再看一遍视频”，而是先把视频变成一种**更容易理解、更便宜读取、更容易组合**的结构化表示。

视频、图片、字幕 / 原声、人物、动作、场景与上下文原本都是高成本的多模态信息。Structure 会把这些信息压成可检索、可排序、可回查的表格和文本层，例如 `frame-observations.csv`、scene / overview 与 `content-map.md`。后续的人、Director 或其他 Skill 可以优先消费这些紧凑数据，而不是每次重新加载原视频、九宫格和大量图片。

这带来一个很直接的变化：

| 过去 | Structure 之后 |
|---|---|
| 一条视频一条视频重新分析 | 把多条视频变成统一的结构化数据层 |
| 想看某个时间点，还要重新打开视频 | 直接定位到时间码对应的人物、动作、对白、背景和内容说明 |
| 不同任务要重复读取同一批多模态素材 | 剪辑、内容研究、效果复盘、检索可以复用同一套结构化结果 |
| 大量上下文消耗在“重新看一遍” | 高成本多模态读取集中到真正需要深挖的区域 |

## 一个最直观的例子：从“分析视频”到“分析内容”

假设你有 500 条已经发布的短视频，同时拿到了播放曲线、停留、跳出或互动数据。

过去通常只能先得到：

> 视频 A 在 12 秒留存上升；视频 B 在 8 秒开始流失；视频 C 完播率较高。

但真正想知道的是：**用户在那个时间点到底看到了什么。**

Structure 之后，每一个已分析时间点都可以对应到结构化内容：人物、动作、表情 / 视线、空间关系、对白、屏幕文字、场景背景和叙事功能。于是用户行为数据可以直接挂到内容节点上：

| 时间点 | 结构化内容 | 内容类型 | 用户表现 |
|---|---|---|---|
| 00:08 | 两人争执，其中一人转身离开 | 冲突 / 动作变化 | 留存上升 |
| 00:12 | 近景反应，无对白 | 人物反应 | 重播增加 |
| 00:19 | 长段解释性对白 | 信息说明 | 流失增加 |
| 00:27 | 前面埋下的信息得到兑现 | 情节兑现 | 留存再次上升 |

这时分析对象就不再只是“哪条视频表现好”，而可以进一步问：

- 哪一类画面更容易产生停留？
- 哪种人物动作经常对应重播？
- 用户流失前通常出现的是长对白、静态画面，还是信息密度下降？
- “冲突 → 反应 → 兑现”这样的结构在不同视频中表现是否稳定？
- 能不能直接找出所有“人物沉默 + 近景反应”的片段，再比较它们的表现？

**Structure 的价值，就是把视频从难以计算和组合的多模态对象，转换成可以检索、筛选、连接、比较和再次创作的数据层。**

同一套结构化结果，不只服务于剪辑，也可以继续用于内容复盘、用户行为分析、跨视频比较、研究、检索和其他 AI 工作流。更完整的示例见 [`examples/content-performance-analysis.md`](examples/content-performance-analysis.md)。

## 核心设计：先压缩，再创作，再把算力花在真正需要的地方

```text
Source footage / transcript / sampled frames
      │
      ▼
① BROAD STRUCTURE
低密度全局理解
      │
      ▼
Compact Structured Representation
Frame Observation Index + scenes + overview + Content Map
      │
      ▼
② DIRECT  ← 人 / research / brainstorming / Director
在独立研究 / 创意环境中形成并确认 Editorial / Script Plan
      │
      ▼
③ DIRECTED DEEP STRUCTURE
只回到脚本命中的原素材区域做高密度多模态回查
      │
      ▼
④ EXECUTE
Verified units → timeline → render manifest → QA
```

这里最重要的不是把所有环节都塞给一个“超级 Skill”。

- **Broad Structure** 先把整个素材面低成本地铺开并压成紧凑表示；
- **Direct** 保留人的创意判断，也可以结合独立的行业 / 主题研究；
- **Directed Deep Structure** 只对确认脚本真正命中的区域重新投入高密度观察；
- **Execute** 把已经验证的内容落到可执行时间轴和工程 QA。

这套设计的目标不是承诺固定比例的 token / 算力节省，而是**避免后续每一步都重新消费昂贵的原始多模态上下文**。

## 适用场景

这套方法适合任何“素材很长、需要反复理解和再利用”的视频工作：剧情 / 综艺 / 访谈 / 纪录片 / 课程 / 活动录像，以及已经发布内容的效果复盘。

它尤其适合以下情况：

- 素材多到无法靠一次摘要可靠理解；
- 同一批视频会被反复用于剪辑、研究、检索或分析；
- 创意方向需要人参与，而不是交给黑箱一次生成；
- 只有少量候选片段值得投入高密度多模态观察；
- 最终还需要把内容判断落实成稳定的时间轴、转场、音轨和 QA。

## 为什么是两轮 Structure

一次把整部长视频扫到帧级既昂贵，也容易在创意方向尚未确定时浪费计算。这里采用两轮不同目标的 Structure：

- **第一轮 Broad Structure：覆盖优先。** 用较低密度看完整素材，并把结果压成可复用的结构化工作层；
- **第二轮 Directed Deep Structure：完整度优先。** 脚本方向确认后，只回到命中的区域补高密度画面、原声、前后语境和反证。

因此，真正昂贵的多模态观察集中在少量高价值区域；而创意讨论、检索和跨视频分析可以尽量基于已经结构化的数据进行。

## Structure 是可复用的工作层

这层结构化数据并不是为了替代原始证据，而是为了让后续工作不必每次从原视频重新开始。它可以被人和其他模型快速浏览、过滤、排序、搜索和引用。

它主要解决三个问题：

- **减少重复多模态读取**：后续 Direct 不需要为了每次创意讨论都重新把原视频、九宫格或大量图片塞进上下文；
- **降低创意阶段的上下文负担**：人工、Director 或其他 Skill 可以直接在 `frame-observations.csv`、scene / overview 和 `content-map.md` 上做组合与判断；
- **把高成本计算集中到命中区域**：只有确认脚本涉及的段落才回到原片进入 Directed Deep Structure，高密度读取画面、原声和前后语境。

这不是把原始证据丢掉。所有结构化记录仍保留 `frame_id`、`scene_id`、时间码、evidence refs 等回查路径，需要时可以重新落回原素材。

## Structure 能做什么

Broad Structure 允许在还没有明确选题时启动。典型产物包括：

- 源素材与版本登记；
- 全时段画面抽样与字幕 / 转写覆盖；
- **Frame Observation Index**：把每张已分析抽样帧的可见事实、人物、动作 / 状态、表情 / 视线、空间关系、环境背景、关键物件、可见文字、邻近对白、内容说明、interpretations 与 unknowns 结构化成表；
- scene 级事件结构；
- 可回查的对白、人物、地点和动作证据；
- source-order overview；
- 跨场景的 Content Map；
- 关系变化、重复线索、关键物件、无声互动等导航；
- coverage 与 unknowns，明确哪些地方只是抽样、哪些已经连续音画核实。

Structure 的目标不是“总结剧情”，而是把原本难以浏览的长视频变成一个**人和模型都能重新检索、组合和回查的素材空间**。

因此 Broad Structure 的正式交付不是“九宫格 + 一个总结”，而是三层：

1. **Raw evidence**：抽样单帧、九宫格、字幕 / ASR、原始定位；
2. **Structured observation layer**：`frames.jsonl` + 人可读的 `frame-observations.csv` + scene cards / `overview.md`；
3. **Creative navigation layer**：`content-map.md`，供人、Director 或其他 Skill 在更完整的信息面上形成 rough plan。

这里的逐帧指 **each analyzed / sampled frame**，不是声称对 25/30fps 的每一个视频帧都做了语义分析。

`deliverable=content_map` 时，可以在这一阶段正式结束，不必进入剪辑。

## Direct 需要什么输入

Direct 默认由外部完成，而且通常适合在一个**独立的研究 / 编导工作区**里完成。它的输入不只可以是 Content Map，也可以包括行业 / 主题研究、平台语境、参考案例和人的经验判断。Structure 的价值，是让这个创意环境优先消费紧凑的表格化信息，而不是反复重新读取原始多模态素材。

本仓库提供两个轻量模板：

- `assets/brief-template.md`：说明这次想表达什么、素材范围和约束；
- `assets/editorial-plan-template.md`：把 research / brainstorming / 编导判断整理成 editorial / script plan。
- 也可以直接引用仓库外的行业研究、主题资料、平台分析或人工笔记；本仓库不强制这些创意输入使用固定格式。

这个阶段可以先形成 rough plan，再通过人工讨论收敛为确认的 editorial / script plan。它不需要已经精确到时间码，但需要把创意结构、外部研究依据、人的关键判断和不能改变的核心表达说清楚，例如：

```text
主题：出去 / 回家

段落1：强调“我可以走”
作用：建立自由和抗拒约束

段落2：真的离开
作用：让表态成为行动

段落3：开始出现“等你回来”
作用：形成反方向力量

段落4：共同生活逐渐稳定
作用：把偶发等待变成关系状态

段落5：一起回去
作用：完成“离开 / 回来”的兑现
```

真正的镜头、对白、时间码、必要前情和保护区间由后续 Directed Deep Structure 完成。

如果你已经有自己的研究 / 编导工作流，可以直接提供现有方案，不必改写成模板。模板只用于保证必要信息不缺失。真正进入 Directed Deep Structure 前，建议明确哪些内容已经由人确认、哪些仍只是待素材验证的假设。

## Directed Deep Structure 为什么单独存在

第一次 Content Map 不应该为了某个主题把所有区域都扫描到帧级；那会非常昂贵，也会让 Structure 变成提前押题。

有了 rough plan 后，系统才知道应该在哪些区域增加信息密度。第二轮仍然先做**完整素材理解**，再做剪辑判断，而不是找到候选后马上标切点。典型动作包括：

- 从十秒级概览抽样提高到一秒一至两张或连续播放；
- 对选中的核心区域建立 **Deep Observation Index**，记录完整画面描述：人物、站位 / 朝向、动作链、表情 / 视线、人物间距离、关键物件、景别 / 构图和画面变化；
- 补充**内容描述**：这一小段实际发生了什么，而不是只抄关键词或台词；
- 补充**场景背景与叙事背景**：地点 / 时间 / 环境、前一事件、为什么会来到这一刻；
- 从字幕关键词回到整段对话核听，记录说话人、对象、语气、停顿、环境声 / 音乐和 audio_verified；
- 从单个场景扩到前后十五至三十秒，必要时继续扩到完整事件，记录 before_state / after_state；
- facts、interpretations、unknowns 分开，并检查 rough plan 的反证、缺口、错误因果和时空关系；
- 最后才把已充分理解的核心区域收敛为 unit、context_ranges、protected_ranges 和可执行剪辑判断。

如果证据与 rough plan 冲突，工具应报告问题并把需要调整的节点返回 Direct，而不是用剪辑技巧强行证明原方案。

## Execute 能做什么

进入 Execute 时，创意方向已经确定，相关素材也经过第二轮定向深挖。后续工作包括：

- 形成可执行 edit plan；
- 建立 assembly timeline 与 output timeline；
- 处理 hard cut / xfade、音轨、文字轨、章节卡；
- 使用 `protected_ranges` 防止剪掉必要语义和动作；
- 编译 `render-manifest.json`；
- 分层缓存视频、音频和文字产物；
- 导出后完整解码、核对帧数和展示时长；
- 扫描近静音；
- 自动生成全部接点对照图；
- 区分技术检查、动态听看和最终成片验收。

当前仓库提供时间轴编译与导出审计脚本，但**不绑定唯一渲染器**。你可以把 `render-manifest.json` 交给 FFmpeg、视频 MCP、剪辑软件适配器或自己的渲染流程。

## 主要文件

```text
long-video-remix/
├── README.md
├── CHANGELOG.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── frame-observation-template.csv
│   ├── deep-observation-template.csv
│   ├── content-map-template.md
│   ├── brief-template.md
│   ├── editorial-plan-template.md
│   ├── project-template.json
│   └── timeline-template.json
├── examples/
│   └── content-performance-analysis.md
├── references/
│   ├── workflow.md
│   ├── data-contracts.md
│   ├── montage-rules.md
│   ├── render-engineering.md
│   ├── qa-handoff.md
│   ├── mcp-adapter.md
│   └── worked-example.md
└── scripts/
    ├── validate_project.py
    ├── compile_render_manifest.py
    └── audit_render.py
```

## 最小使用方式

### 只做 Structure

1. 复制 `assets/project-template.json` 为项目目录中的 `project.json`；
2. 登记 sources 和实际可用工具；
3. 完成 Broad Structure，并同时保留 `frames.jsonl` 与人可读的 `frame-observations.csv`（可复制 `assets/frame-observation-template.csv`）；
4. 在逐抽样帧观察之上形成 scene / `overview.md` / `content-map.md`，可参考 `assets/content-map-template.md`；
5. 将 `project.deliverable` 设为 `content_map` 即可在这里交付。

### 做完整 Remix

1. 先完成 Broad Structure 和 Content Map；
2. 由人 / Director 基于 Content Map 形成 brief 和 rough editorial plan；
3. 把 rough plan 接回项目；
4. 对计划涉及的区域进行 Directed Deep Structure，并生成 `deep-observations.csv`（可复制 `assets/deep-observation-template.csv`），把核心区域的画面、内容、背景、前后状态和原声证据补全；
5. 再把已充分理解的核心区域收敛为 verified units / protected ranges，证据充分后形成 edit plan 和 timeline；
6. 运行：

```text
python3 scripts/validate_project.py 项目目录
python3 scripts/compile_render_manifest.py 项目目录
```

7. 使用实际渲染器生成视频后运行：

```text
python3 scripts/audit_render.py 成片.mp4 项目目录/render-manifest.json --outdir 核查目录 --contacts
```

## 边界

- 抽帧负责发现，不等于连续观看；
- 字幕 / ASR 负责检索，不等于核听原声；
- Content Map 负责扩大人的可见范围，不替代创意判断；
- rough plan 是编导意图，不等于已经得到素材证明；
- Directed Deep Structure 负责把编导判断重新压回原片证据；
- 工具可以建议某个节点的素材不足或替代片段，但默认不擅自改写已经确认的核心表达；
- 渲染成功日志不等于成片通过验收。

## 当前状态

这套仓库更接近一个 **AI-native long-video analysis + remix execution framework**，而不是自动生成短视频的一键工具。

它最适合放在“内容理解”和“实际剪辑工程”之间：先把长素材变得看得见，再把人的创意可靠地做出来。

## License

MIT License。你可以使用、修改和再分发本项目；保留原始版权与许可声明即可。详见 `LICENSE`。
