# 修复明显命令行窗口

## Goal

修复 GUI 转换过程中外部命令行工具弹出明显命令行窗口的问题。无论转换成功、转换失败、解密失败或探测失败，都不应出现 CMD/控制台窗口，只保留 GUI 内的结果提示。

## What I already know

* 用户反馈：“还是有很明显的命令行窗口”“不论成功还是失败，都不要弹出命令行窗口”。
* 外部 CLI 调用集中在：
  * `app/converter.py`：`ffprobe`、`ffmpeg`
  * `app/decryptor.py`：`MusicDecrypto`
* 当前代码已通过 `hidden_subprocess_kwargs()` 给 `subprocess.run()` 传入 `CREATE_NO_WINDOW`。
* Windows 下仅设置 `CREATE_NO_WINDOW` 可能仍不足以覆盖所有可见窗口场景；应同时设置 `STARTUPINFO` 的 `STARTF_USESHOWWINDOW` + `SW_HIDE` 来明确隐藏子进程窗口。
* `music_converter.spec` 已设置 `console=False`，主 GUI exe 不应自带控制台。
* 当前工作区存在与本任务无关/既有的 GUI、converter 和 test_converter 未提交改动；本任务只应最小修改隐藏外部子进程窗口的工具函数与对应测试。

## Requirements

* 所有外部 CLI 子进程调用在 Windows GUI 下隐藏命令行窗口。
* 成功、失败、解密失败、ffprobe 失败等路径都不弹出 CMD/控制台窗口。
* 保持现有 `subprocess.run(..., capture_output=True, text=True, **hidden_subprocess_kwargs())` 调用方式不变，避免分散硬编码 Windows 参数。
* 非 Windows 平台不传 Windows-only 参数，避免跨平台报错。
* 不修改音频转换、解密、GUI 交互等业务行为。

## Acceptance Criteria

* [ ] `hidden_subprocess_kwargs()` 在 Windows 下返回 `creationflags=subprocess.CREATE_NO_WINDOW`。
* [ ] `hidden_subprocess_kwargs()` 在 Windows 下同时返回已设置 `STARTF_USESHOWWINDOW` 和 `SW_HIDE` 的 `startupinfo`。
* [ ] `hidden_subprocess_kwargs()` 在非 Windows 下仍返回 `{}`。
* [ ] `ffprobe`、`ffmpeg`、`MusicDecrypto` 的现有调用继续使用统一 helper。
* [ ] 单元测试覆盖 Windows/非 Windows 分支。
* [ ] `python -m unittest discover -s tests` 通过。
* [ ] `python -m compileall app tests` 通过。

## Technical Approach

* 在 `app/subprocess_utils.py` 中增强 `hidden_subprocess_kwargs()`：Windows 下创建 `subprocess.STARTUPINFO()`，设置 `dwFlags |= subprocess.STARTF_USESHOWWINDOW`，设置 `wShowWindow = subprocess.SW_HIDE`，并保留 `CREATE_NO_WINDOW`。
* 将返回类型从只允许 `int` 调整为可容纳 `startupinfo` 对象的类型。
* 更新 `tests/test_subprocess_utils.py`，通过 mock 验证 Windows 分支同时传递 `creationflags` 和 `startupinfo`，非 Windows 分支不变。

## Decision (ADR-lite)

**Context**: 仅使用 `CREATE_NO_WINDOW` 仍可能让外部 CLI 在 Windows GUI 中出现可见命令行窗口。

**Decision**: 继续集中使用 `hidden_subprocess_kwargs()`，但在 Windows 下同时设置 `CREATE_NO_WINDOW` 与 `STARTUPINFO(SW_HIDE)`。

**Consequences**: 调用点无需变化，隐藏窗口策略集中维护；测试需要从仅比较 dict 数值改为检查 `startupinfo` 属性。

## Out of Scope

* 不重做 GUI。
* 不改转换流程、解密流程或错误文案。
* 不重新打包或发布 exe；如需验证打包产物，应在代码修复后单独构建测试。

## Technical Notes

* 已检查：`app/subprocess_utils.py`、`app/converter.py`、`app/decryptor.py`、`music_converter.spec`、`tests/test_subprocess_utils.py`。
* 相关 spec：`.trellis/spec/backend/quality-guidelines.md` 中 “Windows GUI external CLI subprocesses”。
