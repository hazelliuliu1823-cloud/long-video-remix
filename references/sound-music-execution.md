# Sound & Music Execution

本文件定义 Direct 2 到 Execute 之间的声音与音乐执行规则。它不新增创意阶段，也不替代 `execution-plan.md`、`timeline.json` 或既有 Dialogue / Edit Boundary 保护；它解决的是：音乐是否可以改变画面节奏、每段声音要怎样处理，以及这些决定如何映射到可调用能力。

## 1. Music Mode Confirmation Gate

Direct 2 在形成正式 Execution Package 前，先推荐并确认 `music_mode` 和声音形式；同一次确认中分别列清这两项。`music_mode` 只允许：

- `narrative_led`：叙事优先。核心画面、对白、停顿和关系变化先锁定，音乐服务已确认叙事。
- `hybrid`：叙事锚点锁定，锚点之间的可调整区域可以服从 beat / phrase / section。默认优先用于既有完整叙事又希望具有短视频音乐节奏的内容。
- `music_led`：音乐结构优先。先确定音乐与 Music Map，再在不违反 Narrative Direction、证据、Edit Boundary 和保护范围的前提下组织候选素材。

### 两轮规则

1. **第一轮由 Director 2 主动判断。** 读取已确认 Narrative Direction、Detail evidence、protected ranges、完整对白 / 动作和可伸缩素材后，推荐模式及声音形式，列出理由、必须保护的事件、可由音乐组织的区域和人声分离决定。不得把选项直接甩给用户代替判断。
2. **第二轮必须有明确确认来源。** 若当前或既有用户指令已经明确指定模式，直接承接并记录 `confirmation_source`，不得重复询问。否则将 `music-direction.json.status` 保持为 `proposed`，向用户给出推荐与 A/B/C 选择后结束当前回合；在用户明确确认前，不得完成 Music Map、按音乐改画面长度、完成最终 AV Mapping、把 Execution Package 标记 confirmed 或进入 Execute。

面向 WorkBuddy / Agent 的默认用户可见回复保持短而明确：先写“建议模式 + 具体理由”，再列“必须保护”“可随音乐调整”，最后只给 `A. 按推荐模式继续 / B. narrative_led / C. music_led`（推荐模式若本身是 B/C，则三项按实际重排，避免重复）。本轮到此结束，不在同一回复继续生成最终 Execution Package。

新项目使用 `assets/music-direction-template.json`。confirmed 状态必须有 `confirmed_mode`、`sound_form`、`dialogue_separation`、`confirmed_by / confirmed_at / confirmation_source`。`sound_form` 定义如下，模式确认不自动代替声音形式确认：

| sound_form | 本条采用的声音形式 |
|---|---|
| source_mix | 保留原节目混音，含其中原乐；不新增配乐 |
| original_voice_only | 保留人物原声及需要的环境声，不留音乐 |
| add_music | 保留规定原声，新增配乐 |
| replace_music | 替换原乐，保护规定原声 |
| designed_silence | 按明确决定设计无声；仍须满足既有对白政策及例外规则 |

`dialogue_separation` 写 `not_needed / required`；required 时必须写具体 `separation_fallback`。已有明确声音决定直接承接，未确定的部分随推荐单独呈现。采用具体音乐时，在完整执行包中列 `music_asset_ref / music_asset_digest` 与 `music_selection`（title、version、source、start_ms、end_ms）；整包确认绑定该文件与区间，模式确认不自动授权后续任意换曲。原节目音乐参与节奏分析时，也提供可检查的提取资产及来源。

项目启用 `music_direction_policy=mode_confirmation_required` **或已经填写 `music_direction_ref`** 时，进入 ready_for_render 必须有有效 confirmed 声音方向，漏写 policy 不能绕过确认。仅保留原声、且不使用音乐组织画面时不要求 Music Map。

## 2. Music Map 与音乐理解

音乐不是默认附着在成片后的装饰。`hybrid` / `music_led` 在采用具体音乐并需要音乐结构参与剪辑时，可用 `assets/music-map-template.json` 保存机器分析与编辑判断。

机器分析可以包含：duration、tempo / BPM、beat positions、onset / strong accents、energy curve、section boundary candidates。可由当前环境中已验证的本地或 MCP 能力完成；Skill 不绑定具体库。分析结果只是候选结构，不自动等同于编辑意义。

Director 2 进一步把候选结构整理为 Music Map：

- **beat / accent**：适合动作落点、快速镜头或局部强调；
- **phrase**：适合一组动作、一个小段情绪或一轮互动完成后换段；
- **section / energy**：适合 intro、build、break、lift、climax、outro 等宏观结构；
- **intentional non-sync**：核心对白、停顿、主动方或关系变化若会被卡点破坏，明确记录“不跟音乐走”。

Music Map 不要求所有镜头卡点。AV Mapping 应分别标出 narrative anchor、music anchor、sync tolerance 和 protected status。保护事件优先级高于音乐对齐。

进入正式执行时，`music_led` 或存在 music-flexible events 必须 `music_map_required=true`。已声明的 Music Map 不能只写 complete：`music_asset_ref` 对应实际音乐文件，`duration_ms` 与实测全文件时长相同；节拍 / 强音位置为时长内递增的唯一毫秒值；sections / phrases 使用 `anchor_id / start_ms / end_ms / label`，同类区间顺序排列且不重叠。至少有一个实际编辑锚点与选用区间相交；不强制每首音乐都存在固定 BPM 或节拍网格。

`av_mapping` 每行写 `event_id / music_ms / sync_tolerance_ms / relationship / reason`，relationship 为 `picture_to_music / music_to_picture / intentional_non_sync`。音乐时间须对应实际锚点或已标注的乐句 / 段落，非同步可用 null；可随音乐调整的事件须有映射，protected event 不得标成 picture_to_music。`qa.analysis_verified=true` 与具体 notes 记录实际核对依据；机器候选不能自行升级为已核实编辑判断。草案阶段允许 Music Map pending，最终执行前才要求 complete / verified 和完整数据。

WAV 时长由本地音频头读取，其他格式使用可用 ffprobe；图片解码按需使用 Pillow。能力缺失则保留草案与可恢复入口，不宣称正式校验通过。文件、音乐区间或 Map 变化须更新受影响决定和授权；脚本只检查声明、一致性与可达性，真实听感仍由试听 QA 判断。

## 3. Audio Treatment Plan

Execution Plan 在最终 `audio_tracks` 之前增加 Audio Treatment Plan，先写“要对声音做什么”，再写处理后的音轨“最终放在哪里”。常用处理动作：

- `preserve`：原声完整保留；
- `isolate`：从原混音中分离需要保留的对白 / 人声；
- `attenuate`：降低原声或背景层，但不删除；
- `replace`：原音乐等被替换为新资产；
- `remove`：该声音不进入成片；
- `designed_silence`：主动创造留白；用事件 / expected quiet range 记录，不伪造成一条不存在的声音轨。

基础执行能力本轮包括 gain、fade、duck、mix、designed silence、loudness normalization，以及按需调用 dialogue separation。EQ、compression、denoise 可作为轻量可听性处理或输出标准化，但不能默认重塑人物原声；dereverb、AI voice reconstruction、复杂空间设计、自动 stem remix 等高级 Sound Design 不作为本轮必需能力。

## 4. Execute 内部顺序

声音仍属于 F Execute，不新增阶段：

1. **Audio Preparation**：extract 必要源音频；按 Treatment preserve / isolate；准备已确认 music asset；必要时产生 derived audio asset。
2. **Audio Assembly**：按成片坐标 place / trim / gain / fade / duck / mix / designed silence / normalize。
3. **AV Render**：与画面共同渲染或 mux；所有成片位置以编译后的 output 坐标为准。
4. **Audio / AV QA**：检查对白完整、分离伪影、残留原 BGM、新音乐压对白、留白是否符合设计、J/L-cut 与动作 / 对象是否错位，以及最终响度 / 低电平扫描。

`timeline.audio_tracks` 继续承载最终音轨及位置，不承担“如何分离”的工作，也不新增 schema。`isolate` 的结果作为 derived asset 引用，保留来源、源区间、操作、实际工具 / 模型（若可得）与 review 状态，不冒充 untouched original audio。

## 5. MCP / Tool Capability

Skill 只依赖抽象能力，不写死后端：

| capability | 作用 | 常见实现方向 |
|---|---|---|
| `extract_audio` | 从授权源按 source range 提取音频 | Media / FFmpeg MCP 或本地工具 |
| `separate_dialogue` | 把需要保留的对白 / 人声从原混音中分离 | 本地 source-separation 后端；Demucs 只是可选实现之一 |
| `analyze_music` | BPM、beat、accent、energy、section candidates | 本地音频分析库或 MCP |
| `mix_audio` | trim / place / gain / fade / duck / mix / normalize | Media / FFmpeg MCP 或本地工具 |
| `inspect_audio` | 核听 / 扫描 / 响度 / 静音与伪影检查 | 当前环境可验证的音频检查工具 + 人工 / 模型核听 |

执行前按 `references/mcp-adapter.md` 做 capability discovery。工具不存在时先复用兼容本地能力；确需准备后端时，先分别核对软件与模型权重许可证，并遵守该文档的大下载说明与独立 venv 规则。`separate_dialogue` 可优先解析到 Demucs 兼容本地后端；`analyze_music` 使用实际环境中许可证兼容的分析实现；基础音频处理优先复用 FFmpeg / Media。准备失败、环境不允许、许可不清楚或涉及付费 / 凭证 / 第三方上传 / 提权时进入 unavailable / fallback；任何情况下都不把“已安装”写成“已执行”。

## 6. QA 与回退

人声分离是可选处理，不是默认步骤。只有在“必须保留人物原声 + 原节目 BGM 与对白粘连 + 本轮确实要去掉 / 替换原 BGM”时才优先触发。分离结果必须核听；文件生成成功不能等同于可用。

如果分离出现缺字、尾音丢失、笑声 / 呼吸被吃掉、明显水声 / 金属伪影或原音乐残留，按 Execution Plan 的 fallback 处理，常见顺序是：调整分离参数或区间 → 降低处理强度 → 保留原混音并调整新音乐策略 → 标记人工处理。不得为追求“干净”而损坏已保护的表演信息。
