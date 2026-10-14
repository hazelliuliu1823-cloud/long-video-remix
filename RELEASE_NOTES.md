# v1.2.2 确认节点修订 / Confirmation Review Revision

2026-10-14。本次保留版本号，在现有安装包上定向修正确认流程。

- 主线、声音形式 / 音乐模式、真实关键帧 Mockup、完整执行包分别呈现确认内容；视觉与整包可同轮确认，已有明确确认直接沿用。
- 新增 visual-confirmation 及强制检查：实图可打开、目标画幅一致、原图可达、图片与参数同版；缺图或未确认只交草案，正式渲染阻断。
- 采用配乐时核对曲目 / 版本 / 区间与实际音乐文件；必要的 Music Map 须有有效时长、锚点、AV Mapping 与核对记录，不能只填 complete。
- 同步独立 handoff、模板、双语提问示例、合成示例与测试；本次不处理项目迁移。

227 项回归测试、Skill 基础校验和合成示例编译 / 授权检查通过。

This revision retains v1.2.2 and adds explicit sound-form and visual approval records. Readable source-frame mockups, their production parameters and output size must match the approved version before formal rendering. Existing explicit choices are reused; missing decisions/assets permit planning only. Adopted music bytes/excerpts and meaningful Music Maps are validated and fingerprinted. Standalone handoff instructions, bilingual prompts and synthetic fixtures are updated; project migration is outside this revision.

---

# v1.2.2 — Capability Auto-Preparation / 能力自准备

2026-10-14

在 v1.2.1 声音与音乐执行上补齐运行时能力准备、许可边界与 Music Direction fail-closed 校验；不新增创作阶段，不把第三方模型权重塞进 Skill 包。

- **Discover → license check → prepare → verify：** capability 缺失时先复用已有 MCP / 本地工具；只有来源明确、许可证允许当前用途且当前 Agent 具备相应权限时，才准备本地后端并以最小样本 smoke test 验证。
- **代码与模型权重分开判断：** Demucs 代码可作为 MIT 许可的可选 `separate_dialogue` 实现；预训练权重、模型卡资源和其他第三方资产分别核对许可。v1.2.2 Release 不打包第三方模型权重，商业使用许可不明确的权重不静默使用。
- **隔离重依赖：** Demucs / PyTorch 等可能带来大体积下载或环境依赖时，先说明影响；Python 类后端默认进入项目独立 venv，不自动修改用户已有全局环境。
- **Music Direction fail-closed：** `music_direction_ref` 一旦存在即启用 Music Mode Gate；即使漏写 `music_direction_policy`，未确认的方案也不能进入 `ready_for_render`。确认后直接修改采用的 Music Map 会使旧授权失效。
- **完整使用示例：** 中英 README 补上 Direct 2 / Execution 两个提问示例；用户可提前声明“音乐模式：narrative_led，不新增配乐”以避免重复确认。
- **示例迁移：** `examples/synthetic-ready` 补入已确认的 `narrative_led` Music Direction，并刷新授权与 render manifest。

200 项工程回归通过；合成示例校验、编译与授权检查通过。真实 WorkBuddy 权限、网络、第三方安装、模型权重许可与真实媒体听感仍须在实际运行环境中确认。

## English

v1.2.2 adds license-aware capability preparation, isolated heavy dependencies, and fail-closed Music Direction validation. Software licences and model-weight licences are checked separately; Demucs code remains an optional MIT-licensed separation backend, but third-party pretrained weights are not bundled in the Release and are not silently treated as commercially usable when their licence is unclear. Heavy Python backends default to a project-local venv. A declared `music_direction_ref` activates the confirmation gate even if the policy field is omitted, and changing an adopted Music Map invalidates the old authorization. The bilingual README now includes Direct 2 and Execute prompt examples. All 200 regression tests pass.

---

# v1.2.1 — 声音与音乐执行 / Sound & Music Execution

2026-10-14

在 v1.2.0 的视觉交付基础上，把声音从“音轨参数”升级为可确认、可执行、可回查的导演与工程链路，同时加入音乐参与组织画面的能力。

- **Music Mode Gate：** Direct 2 必须先主动推荐 `narrative_led / hybrid / music_led`。已有明确用户选择时直接承接；否则只输出推荐、保护节点、可随音乐调整区域和 A/B/C，停在 `proposed` 等待明确确认。
- **Music-Aware Editing：** `hybrid / music_led` 可使用 Music Map，把 beat / accent / phrase / section / energy 与 narrative anchors 映射；保护对白、动作链、主动方和关系变化优先于卡点。
- **Audio Treatment：** Execution Plan 增加 preserve / isolate / attenuate / replace / remove / designed silence，基础执行覆盖 gain / fade / duck / mix / normalize；人声分离按需触发，结果作为 derived asset 保存并核听。
- **MCP 抽象能力：** 新增 `extract_audio / separate_dialogue / analyze_music / mix_audio / inspect_audio`。Skill 不把 Demucs、具体音乐分析库或具体 FFmpeg MCP 写成硬依赖，运行时按 capability-map 发现并验证。
- **机械门槛：** 新项目默认启用 `music_direction_policy=mode_confirmation_required`。未确认 mode 阻断 ready_for_render；music-direction 与采用 Music Map 进入 Direct 2 授权指纹，确认后改动会使旧授权失效。旧 v1.2.0 项目未声明该 policy 时保持兼容。

新增 `assets/music-direction-template.json`、`assets/music-map-template.json` 与 `references/sound-music-execution.md`；正式 timeline schema 与既有 Structure CSV 表头不变。196 项工程回归通过；新增检查覆盖 proposed / missing gate、确认后改动失效和 required Music Map。真实音乐审美、分离听感与最终混音仍需实际试听，不由静态测试替代。

## English

v1.2.1 adds a mandatory Music Mode decision for new projects, music-aware editing, executable Audio Treatment, and backend-agnostic audio MCP capabilities. Direct 2 recommends `narrative_led / hybrid / music_led` first; a prior explicit user choice is reused, otherwise the workflow stops at `proposed` until confirmation. Confirmed music-direction and any adopted Music Map are bound into Direct 2 authorization. Existing v1.2.0 projects remain compatible unless they opt into the new policy. All 196 regression tests pass; real listening and mix quality still require playback review.

---

# v1.2.0 — 关键帧与视觉样稿交付 / Keyframe Mockup Handoff

2026-10-08

在 v1.1.0 基础上，把 Direct 2 的视觉设计显性化，并让后续执行复用同一套设计。

- **Detail 原图交付：** 核心关键帧单独保存，连同清单和 handoff 交给 Direct 2。
- **Direct 2 视觉样稿：** 用真实关键帧、实际文字和目标输出画幅制作可打开的 mockup；一两个代表样稿锁定整体风格，实际采用的相片页 / 录像框等版式纳入样稿。
- **执行可复现：** Execution Package 同时交付字体、布局参数、必要资源和布局源文件或渲染方法；Execute 复用这些内容；mockup 的核心是锁定风格，QA 核对成片与 mockup 风格是否匹配，不要求逐帧或逐像素对应。缺失样稿明确待补。商用发布时注意字体授权。

更新现有规范与模板，不增加文件、创作阶段或脚本，不改正式 CSV 表头及 schema。SKILL.md 为 23,447 / 23,842 字节；192 项工程回归通过。**本版新增的视觉交付内容几乎没有自动化检查**：唯一的机器检查是进入 ready_for_render 时若未登记任何 mockup / 参考图，给出提醒（不阻断）；样稿质量与风格是否匹配仍须人工审阅，工程回归不代替真实视频的视觉验收。

审阅修复（同为 v1.2.0）：验收标准由“像素级复现”改为“风格匹配”；mockup 规则集中写在 `references/execution-package.md`，其他文档与模板只保留字段或摘要（handoff 模板为可独立阅读保留简短完整说明）；增加字体授权风险提示；补齐本版 QA 记录。迁移见 [INSTALL.md](INSTALL.md)。

## English

Built on v1.1.0. Detail hands over individual original keyframes. Direct 2 produces actual full-canvas mockups from those frames and the intended text, with typography, layout parameters, required resources and a reusable layout source or rendering method. One or two representative samples normally establish the film's style; show special layouts when used.

Execute reuses the same design and resources. Mockups exist to lock the style: QA checks that the output matches the mockup's style, with no frame-exact or pixel-exact requirement. Missing mockups remain explicitly pending. Check font licences before commercial release. Existing instructions and templates are updated without adding package files, creative stages or scripts, or changing formal CSV headers or schema versions. All 192 engineering tests pass. The new visual handoff has almost no automated checks: the only one is a non-blocking reminder at ready_for_render when no mockup or reference image is declared; mockup quality and style match still need human review. A review round in v1.2.0 replaced pixel-level wording with style matching, consolidated the mockup rules in `references/execution-package.md`, added the font-licence note and the v1.2.0 QA record. See [INSTALL.md](INSTALL.md).

---

# v1.1.0 — 以 v1.0.7 为底的精简版 / Lean Detail Rebuild

2026-10-07

回到 v1.0.7，只加有证据支撑的四件事，并给 SKILL.md 设了大小上限。v1.0.8–v1.0.10 的开发线不再沿用。

## 改了什么

- **抽帧时间标签实测。** 本地原片优先用 `scripts/extract_frames.py`；其他环境按 MCP 适配保留实测时间与源绑定，不按序号计算。`signals` 给出变化与声音候选，`strip` 给出逐帧条。目录清理只处理专用标识中登记的输出，并保护项目与源文件目录。
- **Detail 取证规则。** 新增只在 E 阶段读取的 `references/detail-evidence.md`：全覆盖、按内容定密度、每个时间点只读一次；细动作不凭缩略图下结论；切点先夹住再逐帧，不靠反复加密逼近。
- **两道门槛。** Detail 文件写到一半就做结构检查；问题闭环按实际关联的节点核对唯一 ID、来源与区间；未解决问题阻止入选节点渲染，被否定的问题须有对应节点的人工确认。
- **SKILL.md 不再变长。** 测试把它锁在 v1.0.7 的大小以内（当前 23,445 / 23,842 字节）。

## 兼容

正式 CSV 表头不变。项目迁移有四项，都在 Detail 完成时检查：自由文本 `target_questions` 改为稳定 `question_id`；观察的节点与其区间一致；问题已填写的来源 / 节点 / 区间与实际关联一致；被否决 / 未解决的问题列入 handoff 的问题闭环表（标题含 Question Closure Ledger 或“问题闭环”即可）。详见 INSTALL，v1.0.8–v1.0.10 项目的处理也在其中。

## 验证

- Python 3.12.14 + FFmpeg 6.1.1 + Pillow：186 项回归全部通过（较 v1.0.7 新增 33 项，其中第一轮审阅修复新增 9 项）。第二轮审阅修复后共 190 项，在 Python 3.12.3 + FFmpeg 6.1.1 + Pillow 上全部通过。
- 抽帧时间测试逐帧解码画面内容核对标签；把实现换回 ffmpeg 默认取整 + 计算标签时，3 项测试失败。
- 合成示例的校验、编译与渲染授权检查通过。
- **尚未在真实长视频上做 benchmark**，读图量与耗时的改善未经证实；请用 `assets/benchmark-template.md` 记录。

---

# v1.1.0 — Lean Detail Rebuild (English)

Back to v1.0.7 plus measured frame timestamps, a Stage-E evidence guide, early Detail lint, a single closure ledger and an instruction-size cap. Review repairs harden directory cleanup and evidence-linked question closure, and clarify MCP adapters; early numeric lint is unchanged. A second review round accepts localized ledger headings with a clear hint when the section is missing, documents all four project migrations (stable question IDs, observation / interval node consistency, question-to-interval consistency, the closure ledger), and specifies how an MCP frame adapter must prove measured timestamps. Formal CSV headers remain unchanged. 190 tests pass; timing tests check decoded picture content. No real long-video benchmark has been run yet.

---

# v1.0.7 — 常用提问示例 / Prompt Examples

2026-10-03

本次更新集中在双语使用说明，帮助使用者按当前任务提出请求，并明确每一阶段应拿到什么。

## 四个常用提问示例

- 还没有选题：先做 Broad Structure，交付结构化观察表、全片概览、Content Map 和覆盖记录。
- Broad 已完成：提出候选创作方向，供人讨论并确认主线。
- 主线已确认：定位需要做 Detail 的区间，交付精查任务单。
- 区间已选好：完成 Detail，交付证据、剪辑边界、真实关键帧与可独立阅读的 handoff。

中英 README 的示例均位于“快速开始”之后。原有首屏、核心价值、流程示意、折叠方法和内容效果分析示例保留。

## 版本与兼容

版本统一为 v1.0.7，安装说明、CHANGELOG 和校验清单同步更新。本次为文档与发布整理，工程脚本、测试、模板、契约、示例、agent 配置及历史 QA 保持原字节。已有项目资料和已确认方案继续复用。

## 实际验证

- Python 3.12.14：153 项回归全部通过。
- 合成示例：静态校验、时间轴编译、渲染授权检查全部通过。
- 文档链接、包内文件校验和与压缩包完整性检查通过。

本次验证不包含真实长视频分析或成片播放；合成示例检查工程链路。

安装与更新见 [INSTALL.md](INSTALL.md)，历史验证记录见 [docs/qa](docs/qa/README.md)。

## English

This documentation release includes four matching Chinese and English prompt examples and their expected deliverables: Broad Structure, creative-direction proposals, targeted Detail intervals, and Detail evidence with a self-contained handoff.

The existing introduction, workflow illustration, core values, folded method, and content-performance example are retained. Engineering scripts, tests, templates, contracts, examples, agent metadata, and historical QA are unchanged.

All 153 regression tests passed under Python 3.12.14. The synthetic example passed validation, timeline compilation, and render-authorization checks. Documentation links, package checksums, and archive integrity were checked. Real-video analysis and playback were not re-tested.

---

# v1.0.6 — Structure Exceptions & Execution Package

本版以 v1.0.5 为底稿，只落实已确认的七项修改：固定字段下明确异常并继续可做部分；Detail 固定交付真实关键帧；Detail 形成独立 handoff 并携带下游完整输出要求；Direct 2 输出完整 Execution Package；少量 reference 锁定全片规则；Execute 接收完整包；原 QA 增加 Reference Compliance。

新增可复用契约与四份模板见 [执行包规范](references/execution-package.md)。通常一两个风格样本即可，不要求每个镜头或字幕对应 reference。关键帧缺失要声明原因 / 影响 / 下游处理，不能用生成图冒充原片，也不能把异常变成渲染豁免。

原有流程、两次 Direct、正式 CSV 表头、证据与时间标签、Edit Boundary、对白保护、授权、渲染算法及分层缓存保留。仅为完整包补充文件 / reference 指纹检查，使制作规则改变时旧确认失效；未声明新 package policy 的旧项目保持原机械行为。机器不证明参考图质量或文档完备性，最终风格按 Reference Compliance 实际对照观看。

安装 / 迁移见 [INSTALL.md](INSTALL.md)，本轮范围与实际验证见 [v1.0.6-QA.md](docs/qa/v1.0.6-QA.md)。

2026年10月2日封版修补（版本仍为 v1.0.6）：核对关键帧与 unit / 已有帧记录的来源和时间一致性；实际关键帧图片纳入输入指纹，图片被覆盖后旧渲染入口须重新编译；unavailable 强制匹配同步异常声明。新增 15 项回归，全部 153 项通过。原工程流程和实现保持不变。

2026年10月2日公开文档整理（版本仍为 v1.0.6）：完整中英 README 保留低成本复用、丰富结构、人工 Direct 与可靠 Execute 的定位；补齐文件树和本地安装命令、英文 description 与素材使用权说明，作者署名统一为 hazelliuliu1823-cloud。历史 QA 归档至 [docs/qa](docs/qa/README.md)，其原始验证记录保留；安装包校验和重新生成。

---

# v1.0.5 — Independent Source Audio Dialogue

长视频先形成可检索、可回查的结构化工作层。后续选题、改稿和多版本剪辑优先复用这层数据，只对命中区域重新进行高密度音画核实，减少重复处理整段多模态素材的开销。人保留两次创意决定，系统根据确认方案完成工程执行。

本版在 v1.0.4 上集中修补 F4：独立源音轨采用的对白没有全面进入整句检查与确认摘要。

- **逐源音轨检查**：卡片上的原声、未列入视频 audio_source_refs 的额外音轨、另一素材仅采用声音，均从实际取段推导已知 utterance。先核对来源、当前版本、audio_verified 和整句核听，再检查保留政策与实际可听覆盖。
- **确认摘要补齐依赖**：音轨独有 utterance 及其专属 review 进入 evidence_digest。确认后改动这些记录会使原确认失效；重新编译也必须检查当前证据资格。
- **合法独立声音继续执行**：完整且已核实的异步对白不强制绑定视频口型；按同源、同 speed 与一致的成片映射，可在多轨 / 卡片间连续保留整句。
- **例外归属明确**：视频原声沿用 event 级同步、保护与例外；独立截句使用 track 级 audio_required_range，明确不保留政策使用 track.dialogue_policy_reason。具体创作决定仍来自已有 Direct 2，不增加创意阶段。

此前 F1—F3 的修补与音轨完整取段核听要求保留。Broad / Detail 分工、六套 Structure 正式表、两次 Direct、Edit Boundary、时间标签、累计量化、分层缓存和 render audit 保留。没有预设成本降幅；抽帧、ASR、定向回看和 GPU 渲染仍需计算资源。

安装 / 迁移见 [INSTALL.md](INSTALL.md)，本轮实际验证见 [v1.0.5-QA.md](docs/qa/v1.0.5-QA.md)。已有 v1.0.4 项目保留全部结构化资料，完成独立对白对账后，按已有创作授权更新 Direct 2 记录并重新编译。

Broad 覆盖、采样与说话人语义证明、Deep 保护转移以及非对白声音的整体收束继续保留原职责边界。合成验证不证明真实长视频理解质量或最终观感；最终听看仍独立记录，外部渲染适配器须接入入口检查。
