# Detail 证据获取：时间标签、读图、切点与问题闭环

只在 E（Directed Deep / Detail Structure）阶段读取。本文件规定**怎样取证**，不改变 Detail 要交付的字段与验证项；字段契约仍见 [data-contracts.md](data-contracts.md)。

## 1. 时间标签：在帧产生时实测写入

- 本地原片且 identity 映射时，抽帧优先用 `scripts/extract_frames.py`。标签是 ffmpeg 实测的 pts，不是"起点 + 序号 × 间隔"。文件名为 `source_id_源毫秒.jpg`，同目录 `frames.jsonl` 记录 `source_ms`、`label_method=measured_pts` 与 source 绑定。
- 之后只引用这些标签，不再换算。拼图格子、Broad 名义时间、字幕时间都只是线索。
- 该脚本只接受本地文件和 `time_mapping.type=identity`；MCP / 远程、代理 / 偏移或缺少本地工具时，按 [MCP 适配](mcp-adapter.md) 校验短段，保留实测媒体时间、canonical source time 与源绑定，不为调用脚本改写既有映射。
- 进入 Detail 时核对一次 source 版本与 time mapping；它们不变就沿用已有标签，变了则旧标签与切点全部失效重做。

```sh
python3 scripts/extract_frames.py PROJECT SRC001 1200000-1260000 --mode signals
python3 scripts/extract_frames.py PROJECT SRC001 1200000-1260000 --mode frames --fps 1
python3 scripts/extract_frames.py PROJECT SRC001 1216200-1216800 --mode strip
```

## 2. 读图：全覆盖、按内容定密度、每个时间点只读一次

先读文字：Broad 逐帧观察、动作候选、字幕 / 转写、目标问题。再对整个 DI 运行 `--mode signals`，得到画面变化时段、硬切候选与有声 / 静音时段（只是候选，不是事实）。

按时段分配密度，每个时段只生成并阅读一种密度，不叠加多层：

| 时段 | 密度 |
|---|---|
| 前后语境 | 0.5fps |
| 核心范围中静止或只在说话的部分 | 1fps（下限） |
| 变化时段、Broad 动作候选、目标问题时间窗 | 4fps |

另有必读全分辨率单帧：关键事实的决定性时刻、说话人 / 对象裁决的口型时刻、切点附近，以及缩略图看不清的文字。

升级按事实类型，不按"再加密一层"：

- 细动作、物件交接、谁对谁做：4fps，再读决定性时刻单帧；仍有歧义看连续视频。
- 表情、视线、反应：读单帧，不靠更密的缩略图。
- 说话人 / 对象：原声、硬字幕与口型单帧综合；ASR 只作定位。
- "没有发生"：必须看覆盖完整机会窗口的连续视频或连续原声。

**细动作不凭缩略图下结论**：肯定或否定一个手部 / 物件动作，至少要读决定性时刻的全分辨率单帧。

停止条件：证据已达该事实类型的标准；或已到连续视频 / 原声仍无法确定，此时写 `unresolved` 并给出具体缺口与下一步核查。不为填满字段而加读；同一批证据可支持多个字段。

## 3. 先裁决目标问题，再做完整 Detail

进入 DI 后先回答 `target_questions` 中会改变后续理解的问题，立即更新 `structure-questions.csv`。之后按已确认的事实完成该 DI 的全部字段；`contradicted` 不取消其余验证，也不改变 D1 / D2 的职责。

## 4. 切点：先夹住，再逐帧

切点在内容理解完成之后再找，方法与看内容不同：

1. **夹住**：从已读抽帧确定边界落在哪两张之间。
2. **逐帧**：对该区间加少量余量运行 `--mode strip`，读这一张逐帧条，直接选出起止帧（误差 ≤ 1 帧）。不要用一轮轮加密抽帧去逼近。
3. **声音边界**：先用 signals 的静音 / 有声时段找说话起止与尾音候选，再回听该短段确认。字幕时间不能当切点。
4. **反应收束**：用 `motion.csv` 中局部变化回落的位置作候选，再用逐帧条确认。
5. 在 `edit-boundaries.csv` 的 `boundary_reason` 写明方法（逐帧条 / 静音检测 / 连续视频）与实际精度，`evidence_refs` 指向对应输出。

## 5. 被否决 / 未解决的问题：handoff 里一张表闭环

问题一律用唯一、稳定的 `question_id`，由 `detail-intervals.target_questions` → `structure-questions.csv` → `deep-observations.question_refs` 串联；每个目标问题至少被本 DI 一条观察回指，明确声明的来源、区间和节点须与实际关联一致。

任何实际关联到 Detail 的 `contradicted` / `unresolved` 问题都列入 `execution-handoff.md` 的 **Question Closure Ledger**（节点与实际关联一致，多个节点用分号分隔；标题须含 Question Closure Ledger 或“问题闭环”）：

| question_id | status | plan_node_id | 处理方式 | confirmed_by |
|---|---|---|---|---|

这是唯一的闭环记录。`unresolved` 还要在问题表写出具体缺口与 `next_check`。进入 `ready_for_render` 时，入选节点不能带 `unresolved` 问题；带 `contradicted` 问题须有具体处理方式和人工 `confirmed_by`。validator 会检查这些条件。

## 6. 执行方式

- 密集读图保持单一上下文，不拆给子代理；脚本、lint、文件生成可以并行。每完成一个 DI 即落盘。
- Detail 文件一出现，`validate_project.py` 就做结构检查（表头、ID、范围、引用、枚举），不必等到 E 完成。
- 用 `assets/benchmark-template.md` 记录读图、返工与写入耗时，校准本文件中的密度与阈值。
