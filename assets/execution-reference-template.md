# Execution Reference

> 与 execution-plan.md 一起构成 Direct 2 的 Execution Package。填写实际确定参数；任务未使用的层写 not_applicable 及原因。参考样本通常一两个，全片复用同一套规则。

## 版本、规格与确认

- 项目 / reference 版本：
- execution-plan.md / Narrative Direction：
- 输出 width × height / fps：
- reference 状态与已有确认来源：
- 原片关键帧清单 / 图片入口：
- selected Aesthetic Mockup（project.visual_mockup_ref；未确认写 null）：
- Executable Proof Frame（project.visual_proof_ref；未确认写 null）：
- visual_gate_status：not_started / mockup_confirmed / awaiting_proof / proof_confirmed / not_applicable
- execution_reference_asset_refs：selected mockup、proof、`capability-map.json`（proof_confirmed 时三者都必须纳入）及其他资源：

## Visual Reproducibility Gate

> Aesthetic Mockup 负责选审美；Executable Proof 负责证明最终 Execute 的真实工具链可以复现。两步可在不同模型 / 会话中完成。模型连续性不要求，工具链连续性要求。

- mockup 基于的真实 keyframe / source timestamp：
- selected mockup 文件 / 确认来源：
- inherited execution toolchain（来自 execution-handoff / capability-map）：
- proof 实际使用的 actual_tool / 版本：
- renderer / layout entrypoint：
- proof 使用的字体 / 布局源文件 / 资源：
- final Execute toolchain / entrypoint：
- toolchain continuity：same / changed（changed 时说明 capability-map 与最终 Execute 如何同步更新；同步前 Gate 不得 confirmed）
- proof frame 文件 / 确认来源：
- Gate 尚未关闭时的缺口与下一步：

## 少量参考锁定的规则

| mockup ID / 实际图片 / 原片 frame_id | style / layout ID、文字层级与画面关系 | 全片应用范围与规则 | 未提供项与原因 |
|---|---|---|---|
|  |  |  |  |

Visual Gate 规则见本 Skill 的 `references/execution-package.md`：一两个 Aesthetic Mockup 只选审美方向；选中后必须由最终 Execute 可访问的同一实际工具链重建 Executable Proof。proof_confirmed 后才把该视觉方案视为可执行。原图独立保留，缺图标待补。

- proof 与正式 Execute 共用的字体（含授权说明；商用注意授权）/ 布局生成入口（布局源文件或渲染代码 / 方法）及资源：
- 仅作说明的箭头 / 标签，与实际进入视频的元素及计划引用：

## 画面规则

- 原片保留方式 / crop / scale / 位置（精确参数）：
- 人物、动作、硬字幕需避让的范围 / 安全边距：
- 色彩与效果处理：
- 情绪强化方式及允许使用的范围：
- 相片页 / 录像框等已采用版式：layout ID、图片置入框 x/y/w/h、crop / fit、边框 / 圆角 / 间距、图层顺序与符号参数（尺寸单位与坐标原点须明确；未采用写 not_applicable）：
- 禁止的处理：

## 文字样式

| style ID / 文字用途 | 字体文件或可用字体名 / 确定替代 | 字号 / 单位 / 字重 | 颜色 / 描边 / 阴影 / 背景 | 位置 / 坐标基准 / 对齐 / 边距 | 行数 / 换行 / 字距 / 行距 | 进入 / 退出动效及 ms 或帧数 | 阅读停留规则 |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

实际文字全文、断行及逐条出现 / 消失事件锚点放在 execution-plan.md，并引用 style ID。不要只交“字幕大一些”或“适当停留”。字重是否可用、字号采用 px / pt / 相对高度必须明确；参数绑定本版输出规格。

## 声音与转场

- 原声 / 环境音 / BGM / 旁白政策和禁止项：
- 每条音轨的源 / 取段 / 放置 / 增益 / 速度 / fade / review refs：见 execution-plan.md 的明确记录。
- 每个接点的类型 / overlap 或 card 帧数：见 execution-plan.md 的接点表。
- 重要停顿、动作 / 回应、对白尾部的保护规则：

## 素材与允许调整

| asset ID / 文件 | 用途 / 来源与版本 | available / unavailable / partial / uncertain | reason / impact / downstream_handling |
|---|---|---|---|
|  |  |  |  |

- 字体和参考图片在执行环境的实际入口：
- 可调整项（与原机器授权的 allowed_adjustments 一致）：
- 不得调整项：
- 封面规格 / 全文 / 源图 / 排版（仅本任务要求时）：

## QA 判据

- 全片文字层级、位置、字号 / 颜色、画面占比是否符合上述规则：
- 正常速度阅读时间、遮挡 / 裁切和手机检查：
- 情绪强调、动效 / 转场与 reference 是否一致：
- 成片风格对照：同一版式的成片截图与 executable proof 的对照入口及结论；selected mockup 只辅助审美核对（风格匹配即可）：
- 原声、保护范围与音轨参数是否实现：
- 实际导出 / reference 对照尚未完成的项：

在原 qa.json checks 中登记 ReferenceCompliance；没有实际观看记 not_tested。具体参数变更同步计划、机器授权与受影响时间轴 / 缓存，不在 Execute 中另行定义风格。
