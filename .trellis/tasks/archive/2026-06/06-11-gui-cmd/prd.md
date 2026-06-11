# 修复 GUI 转换时 CMD 弹窗

## Goal

在 Windows GUI / 打包后的桌面应用中执行音频转换时，不再为每次外部工具调用弹出 CMD 控制台窗口，避免打断用户操作。

## What I already know

* 用户反馈：使用 GUI 时出现明显 CMD 弹窗，并且每个转换都会出现，影响使用。
* 项目使用 tkinter GUI，转换链路在 `app.converter` 中调用 `ffprobe` 和 `ffmpeg`。
* 加密音频解密链路在 `app.decryptor` 中调用 `MusicDecrypto` CLI。
* 当前外部命令均通过 `subprocess.run(..., capture_output=True, text=True)` 调用，未设置 Windows 隐藏控制台窗口参数。
* 在 Windows GUI 程序中启动控制台子进程时，如果未显式隐藏窗口，可能出现短暂 CMD 弹窗。

## Requirements

* 在 Windows 上，GUI 转换调用 `ffprobe` / `ffmpeg` 时不得显示 CMD 控制台窗口。
* 加密音频解密调用外部 CLI 时也不得显示 CMD 控制台窗口，避免同类弹窗残留。
* 非 Windows 平台行为保持不变。
* 保持现有转换、错误处理、输出解析逻辑不变。

## Acceptance Criteria

* [ ] Windows 下转换普通音频时，`ffprobe` 和 `ffmpeg` 子进程以隐藏窗口方式启动。
* [ ] Windows 下转换加密音频时，解密 CLI 子进程也以隐藏窗口方式启动。
* [ ] 非 Windows 平台不传入 Windows 专用 `creationflags`。
* [ ] 现有单元测试通过。
* [ ] 新增或更新测试覆盖子进程隐藏窗口参数。

## Definition of Done

* Tests added/updated where appropriate.
* Unit tests green.
* Compile check green.
* 不改动与 CMD 弹窗无关的 GUI 布局、转换流程或打包配置。

## Technical Approach

新增一个小的内部工具函数，统一生成 `subprocess.run` 的 Windows 专用参数：在 `os.name == "nt"` 且 `subprocess.CREATE_NO_WINDOW` 可用时传入 `creationflags=subprocess.CREATE_NO_WINDOW`；其他平台返回空参数。`converter.py` 和 `decryptor.py` 的外部命令调用复用该函数。

## Decision (ADR-lite)

**Context**: 多处外部 CLI 调用都会触发 Windows 控制台窗口，若分别硬编码参数容易遗漏。

**Decision**: 使用最小共享工具函数集中处理 Windows 子进程隐藏窗口参数。

**Consequences**: 普通转换和加密解密共享同一行为；非 Windows 平台无额外影响；后续新增外部 CLI 调用可复用同一函数。

## Out of Scope

* 不重做转换队列、进度显示或 GUI 线程模型。
* 不更换 ffmpeg / ffprobe / MusicDecrypto。
* 不修改 PyInstaller 打包模式，除非验证发现代码修复不足。

## Technical Notes

* 相关代码：`app/converter.py`、`app/decryptor.py`。
* 相关测试：`tests/test_converter.py`、`tests/test_decryptor.py`。
* 相关规范：`.trellis/spec/backend/index.md`、`.trellis/spec/backend/quality-guidelines.md`。
