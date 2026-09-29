# long-video-remix

> **Turn hours of footage into a searchable content map — then turn human editorial intent into an executable remix timeline.**

`long-video-remix` 是一套面向长视频、多集素材和长时段活动视频的 AI 辅助分析与剪辑执行工作流。它先把难以浏览的长素材变成**可检索、可回查、带证据的内容地图**，再把人的编导意图重新压回原素材，落实成具体到场景、对白、时间码和保护区间的剪辑方案。

**它不是“一句话自动生成短视频”的黑箱工具。** 它更关注两件更稳定、也更难做好的事：

1. **Structure**：先把几个小时的素材整理成可检索、可回查、带证据的内容地图；
2. **Execute**：在人或独立编导流程给出内容方向后，重新回到原素材做定向深挖，把 rough plan 落成可执行的剪辑时间轴，并完成渲染前后的工程检查。

中间的 **Direct** ——“到底值得讲什么、为什么这样讲、哪条叙事更有意思”——属于创意核心。它可以由人完成，也可以通过 brainstorming、独立 Director Agent 或其他策划流程完成。本仓库会提供输入模板和证据支持，但默认不替代这一层创意判断。


## 为什么做这个

长视频真正难的通常不是“会不会切”，而是两件事：**先看全，再看细**。

- 几小时素材无法靠一次摘要可靠理解；
- 创意方向确定之前，不应该为了某个主题过早把所有区域扫到帧级；
- rough plan 形成之后，又必须重新回到原片提高观察密度，核对语境、对白、动作和因果；
- 最终还要把内容判断转换成稳定的时间轴、转场、音轨和 QA。

这个仓库把这条链路拆开：**Broad Structure → Human Direct → Directed Deep Structure → Execute**。

特别适合：剧情 / 综艺 / 访谈 / 纪录片 / 课程 / 活动录像等长素材的二次创作与主题混剪。

## 核心流程

```text
Source footage
      │
      ▼
① BROAD STRUCTURE
全量粗覆盖：场景、对白、人物、事件、关系变化、可见动作、未确认区域
      │
      ▼
Content Map
可检索、可回查的素材地图
      │
      ▼
② DIRECT  ← 人 / brainstorming / Director
Brief + Rough Editorial Plan
决定想讲什么、段落功能和大致重组逻辑
      │
      ▼
③ DIRECTED DEEP STRUCTURE
带着 rough plan 回到原素材
提高抽样与观察密度、补前后文、核听原声、形成更细 unit / protected ranges
      │
      ├── 证据不足或原计划不成立 ──→ 返回 Direct 调整 rough plan
      │
      ▼
④ EXECUTE
锁定片段 → 时间轴 → 转场 / 音轨 / 文字 → render manifest → 导出审计 / QA
```

这里的 Structure 不是只做一次。

第一轮 Structure 追求**广覆盖**：先把整体素材面展开，让人知道“这里到底有什么”。

Direct 形成 rough plan 后，第二轮 Structure 追求**定向高密度**：重新进入相关场景和上下文，把第一次粗结构中不需要做到的细节补齐，直到计划可以安全进入剪辑执行。

因此它不是简单的 `Structure → Direct → Execute` 单向流水线，而是：

> **先展开整个素材空间 → 人做创意判断 → 再定向回到素材深挖 → 最终收敛成剪辑执行。**

## Structure 能做什么

Broad Structure 允许在还没有明确选题时启动。典型产物包括：

- 源素材与版本登记；
- 全时段画面抽样与字幕 / 转写覆盖；
- scene 级事件结构；
- 可回查的对白、人物、地点和动作证据；
- source-order overview；
- 跨场景的 Content Map；
- 关系变化、重复线索、关键物件、无声互动等导航；
- coverage 与 unknowns，明确哪些地方只是抽样、哪些已经连续音画核实。

Structure 的目标不是“总结剧情”，而是把原本难以浏览的长视频变成一个**人和模型都能重新检索、组合和回查的素材空间**。

`deliverable=content_map` 时，可以在这一阶段正式结束，不必进入剪辑。

## Direct 需要什么输入

Direct 默认由外部完成。本仓库提供两个轻量模板：

- `assets/brief-template.md`：说明这次想表达什么、素材范围和约束；
- `assets/editorial-plan-template.md`：把 brainstorming 或编导判断整理成 rough editorial plan。

rough plan 不需要已经精确到时间码。它只需要把创意结构说清楚，例如：

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

如果你已经有自己的编导工作流，可以直接提供现有方案，不必改写成模板。模板只用于保证必要信息不缺失。

## Directed Deep Structure 为什么单独存在

第一次 Content Map 不应该为了某个主题把所有区域都扫描到帧级；那会非常昂贵，也会让 Structure 变成提前押题。

有了 rough plan 后，系统才知道应该在哪些区域增加信息密度，例如：

- 从十秒级概览抽样提高到一秒一至两张或连续播放；
- 从字幕关键词回到整段对话核听；
- 从单个场景扩到前后十五至三十秒，必要时继续扩到完整事件；
- 核对说话人、被说话人、否定、条件、停顿和动作后果；
- 形成 unit、context_ranges、protected_ranges；
- 检查 rough plan 的反证、缺口和错误因果。

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
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── content-map-template.md
│   ├── brief-template.md
│   ├── editorial-plan-template.md
│   ├── project-template.json
│   └── timeline-template.json
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
3. 完成 Broad Structure；
4. 可参考 `assets/content-map-template.md` 生成 `overview.md`、`content-map.md`、scenes / transcript / coverage 等证据文件；
5. 将 `project.deliverable` 设为 `content_map` 即可在这里交付。

### 做完整 Remix

1. 先完成 Broad Structure 和 Content Map；
2. 由人 / Director 基于 Content Map 形成 brief 和 rough editorial plan；
3. 把 rough plan 接回项目；
4. 对计划涉及的区域进行 Directed Deep Structure；
5. 证据充分后形成 edit plan 和 timeline；
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
