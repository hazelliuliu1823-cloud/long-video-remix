# Blender → FFmpeg 工程示例

这是合成素材工程测试，不是实际影视案例。生成器复用 synthetic-ready 的虚构证据与时间轴，创建两张简单图形和测试音，演示组缩放、末尾状态保持、接点双侧预览、可编辑工程和最终回接。

示例中的项目方法使用 `PM001`，并显式引用知识库 `M13` 与 fallback `F09`，用于演示 v1.3.1 的 `library_refs` / `fallback_refs`；这里的 PM001 是当前项目方法实例，不与知识库 M01–M14 混用。

```sh
python examples/composition-smoke/build_fixture.py /absolute/path/to/new-smoke-project
python scripts/workflow_control.py status /absolute/path/to/new-smoke-project
python scripts/workflow_control.py guard /absolute/path/to/new-smoke-project --action build_composition
```

生成器不写确认，不授予渲染许可；最后一条应被阻断。按 [制作流程](../../references/visual-production.md) 展示实际方案、记录真实决定后才继续。

自动化真实渲染回归位于 tests/test_visual_pipeline.py。设置 BLENDER_EXECUTABLE 后运行相应 integration test。测试里的审批记录明确标为 simulated fixture decisions，只验证机械门槛，不代表用户确认或真实审美验收；测试在临时目录中运行，不修改此示例。
