# Execution Package · Editorial Execution Plan

> 第二次 Direct 的输出之一。输入是 Detail 的 evidence package、真实关键帧和独立 handoff；与 execution-reference.md、素材 / 约束和原机器授权一起构成完整 Execution Package。Execute 只落实确认后的包。

## 最终主线

- thesis / narrative spine：
- 与第一次 Narrative Direction 的变化（如有）：
- 变化依据：

## Music Mode Confirmation Gate

- music-direction ref：music-direction.json
- Director 2 推荐模式：narrative_led / hybrid / music_led
- 推荐理由：
- 必须保护的 narrative event IDs：
- 可由音乐组织 / 调整的 event IDs 或区间：
- 当前状态：proposed / confirmed
- 明确确认来源（已有用户指令可直接承接，不重复询问）：
- confirmed mode / confirmed_by：
- sound_form（source_mix / original_voice_only / add_music / replace_music / designed_silence）：
- dialogue_separation（not_needed / required）与 required 时的回退：
- music asset / music-map ref（如需）：
- 具体曲目 / 版本 / 来源 / 音乐文件指纹 / 使用区间（随整包确认）：

> 若只有 Director 2 推断而没有既有明确用户确认，本轮必须先输出推荐并停住；确认前不得完成最终 AV Mapping、把本执行包标记 confirmed 或进入 Execute。

## 最终素材取舍

### Segment 1
- selected verified unit(s)：
- adopted utterance IDs / adopted_utterance_refs：
- selected Deep observation(s) / observation_id：
- adopted source range(s)：
- selected edit boundary / boundary_id：
- chosen in / out：
- safe in / out windows：
- must-keep range(s)：
- boundary override：no / yes
- boundary override reason（仅 yes 时）：
- boundary override review refs（仅 yes 时）：
- narrative function：
- 必须保留的 context / protected ranges：
- 原声 / BGM / ambience 策略：
- 每条源音轨完整取段及 audio review_refs（含 J/L-cut 扩展）：
- 独立声音的完整 utterance、成片放置、track 级截句例外 / 政策原因（如有）：
- 文字意图（如有）：
- 预计时长：
- transition / time cue：

### Segment 2
- selected verified unit(s)：
- adopted utterance IDs / adopted_utterance_refs：
- selected Deep observation(s) / observation_id：
- adopted source range(s)：
- selected edit boundary / boundary_id：
- chosen in / out：
- safe in / out windows：
- must-keep range(s)：
- boundary override：no / yes
- boundary override reason（仅 yes 时）：
- boundary override review refs（仅 yes 时）：
- narrative function：
- 必须保留的 context / protected ranges：
- 原声 / BGM / ambience 策略：
- 每条源音轨完整取段及 audio review_refs（含 J/L-cut 扩展）：
- 独立声音的完整 utterance、成片放置、track 级截句例外 / 政策原因（如有）：
- 文字意图（如有）：
- 预计时长：
- transition / time cue：

> 按需要继续增加。

## 逐段执行坐标与画面处理

| event ID / 顺序 | unit / source ID | source in/out ms | speed / crop / scale / 画面位置 | assembly 预计帧 / event anchor | 本段文字 / 声音 / 转场引用 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 逐条文字事件

| text ID / 用途 | 逐字全文 / 明确断行 | anchor event ID | local in/out frames | style ID（reference） | 进入 / 退出动效与帧数 | 实际阅读停留 / 保护的重点 |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## Music Map / AV Mapping（按 confirmed mode 需要时）

- music-map ref：
- 音乐分析状态 / 方法：
- section / phrase / beat / accent 中实际采用的编辑锚点：

| narrative event / 区域 | protected / flexible | music anchor（section / phrase / beat / accent / none） | sync tolerance | 画面跟音乐 / 音乐跟画面 / intentional non-sync | 理由 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Audio Treatment Plan

| audio ID / event | 声音内容与叙事作用 | treatment（preserve / isolate / attenuate / replace / remove / designed_silence） | 预处理 / capability | 最终放置与动态处理 | fallback / QA |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 音轨与接点

| track ID / narrative role | source / derived asset ID | source in/out ms | event anchor / local frames 或显式 output 坐标 | gain dB / speed / fade ms / duck | review refs / 同步 / 完整对白保护 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

| 前后 event ID | cut / fade / card 等 | overlap 或独立 card 帧数 | 接续理由 / 保护范围 |
|---|---|---|---|
|  |  |  |  |

## 时长与节奏分配

- 总时长目标：
- 各段预算：
- 必须保留的完整动作 / 对白：

## 执行边界

- 可替换素材：
- 可调整顺序 / 时长：
- Execute 不得改变：

## Evidence check

- pending / contradicted 节点：
- counterevidence 已处理：
- 可进入 Execute：yes / no

## 同包制作参考与 QA

- execution_reference_ref：execution-reference.md
- execution_reference_asset_refs：实际采用的 mockup；草案缺图写 []，正式执行前补齐并确认。
- visual_confirmation_ref：visual-confirmation.json；逐项展示 Mockup 与参数的版本、应用范围和明确确认来源。
- 视觉状态 proposed / confirmed；是否与完整执行包同轮确认：
- 具体文字 / 画面 / 声音 / 转场规则及资产入口：见同包 reference。
- Reference Application Rules：样本提炼为全片规则，不要求每个字幕 / 镜头单独配对。
- QA：原内容 / 技术 / 听看项 + ReferenceCompliance，未实看保持 not_tested。
- exceptions 与下游处理：

## 机器可读执行授权（v1.0.6）

- execution_authorization_ref：execution-authorization.json
- authorization_id / version：
- confirmed_by：
- 完整执行包确认来源（最终取舍、顺序、文字、声音、时长、允许调整）：
- selected_events / sequence：
- allowed_units / allowed_boundaries：
- allowed_adjustments（逐 event）：
- event_specs / audio_specs / text_specs / transitions：
- source_bindings / evidence_digest / Direct 文档指纹：
- execution_reference_digest / execution_reference_asset_digests：
- visual_confirmation_digest / music_direction_digest / music_asset_digest / music_map_digest：
- preserve_dialogue / 删句例外 / dialogue_policy_reason（明确改变政策时）：

先用 prepare_execution_authorization.py 生成 draft，再根据本轮已确认决定核对并记录；草稿不能自动升为 confirmed。发生实际证据变化须回查，发生方案变化须按已有用户授权重新裁决，不能仅重算指纹掩盖变化。详见 references/execution-integrity.md。
