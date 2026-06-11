# 音乐格式转换器 exe

## Goal

做一个面向 Windows 的音乐格式转换程序，优先使用成熟开源能力而不是自己实现编解码，最终能导出可分发的 `exe`。

## What I already know

- 用户希望先充分调研，再制定计划
- 目标是“任意格式音乐转任意格式”
- 最终交付物希望是可迁移的 `exe`
- 用户强调首版要保持轻量化
- 用户强调分发后尽量可迁移、少依赖环境
- 目标用户是完全不懂技术的普通用户
- 当前仓库几乎为空，适合从零搭建 MVP
- 从技术调研看，核心转码引擎最适合采用 `FFmpeg`
- `pydub` 和 `ffmpeg-python` 本质都仍依赖 FFmpeg，不适合作为首版唯一核心能力
- 对首版 MVP，Python 直接调用 `ffmpeg` / `ffprobe` 比再套一层封装更简单
- `PyInstaller` 可以打包 Windows `exe`，更适合这个项目的首版路线

## Assumptions (temporary)

- 首版只面向 Windows
- 首版处理音频文件，不处理视频转音频
- “任意格式”先收敛为“常见音频格式集合”
- 首版先做便携工具，不先做安装器

## Open Questions

- 暂无

## Requirements (evolving)

- 使用成熟开源方案完成常见音频格式互转
- 首版范围明确限定为常见音频格式，不承诺冷门、私有或 DRM 格式
- 最终可导出 Windows `exe`
- 分发方案优先在“轻量化”和“开箱即用”之间做现实平衡
- 面向普通用户，首版内置 `ffmpeg` / `ffprobe`，避免额外环境依赖
- 程序需具备图形界面，而不是只提供命令行
- 首版不支持拖拽导入，只通过按钮选择文件
- 支持单文件与批量转换
- 支持整文件夹导入用于批量转换，并递归扫描子文件夹中的音频文件
- 文件夹批量转换时保留原目录结构输出
- 支持选择输出格式与输出目录
- 首版界面优先最小可用，不开放比特率、采样率、声道等高级参数
- 批量转换遇到输出重名时，默认自动重命名，不覆盖已有文件
- 批量转换中单个文件失败时，继续处理剩余文件，并在结束后汇总结果
- 首版批量转换采用顺序执行，不支持并发转换
- 启动时默认优先使用内置 `ffmpeg` / `ffprobe`
- 首版支持的输入格式至少包括：`mp3` `wav` `flac` `m4a` `aac` `ogg` `opus` `wma`
- 首版支持的输出格式至少包括：`mp3` `wav` `flac` `m4a` `aac` `ogg` `opus`

## Acceptance Criteria (evolving)

- [ ] 能在 Windows 上选择一个常见音频文件并转换为目标格式
- [ ] 能批量转换多个常见音频文件
- [ ] 能通过选择整文件夹递归扫描子文件夹并发起批量转换
- [ ] 文件夹批量转换时能按原目录结构输出结果
- [ ] 不支持的输入格式或转换失败时能给出可读错误信息
- [ ] 用户可选择输出目录和输出格式
- [ ] 首版不依赖拖拽也可完成全部主流程
- [ ] 首版界面无需用户理解高级音频参数即可完成转换
- [ ] 批量转换遇到重名输出文件时，不会覆盖原文件
- [ ] 批量转换中单个文件失败时，其他文件仍会继续处理，并能看到失败列表
- [ ] 程序能直接使用内置 `ffmpeg` / `ffprobe` 完成转换，无需用户配置环境
- [ ] 可生成可分发的 Windows `exe`

## Definition of Done (team quality bar)

- 有最小可用图形界面
- 转换主流程可验证
- 打包流程可复现
- 关键依赖和分发注意事项有文档说明

## Out of Scope (explicit)

- 自己实现音频编解码器
- 首版承诺支持所有冷门、私有或 DRM 格式
- 首版处理视频转音频
- 首版直接覆盖跨平台发布
- 首版包含复杂音频编辑能力（剪辑、混音、特效）
- 首版开放比特率、采样率、声道等高级参数设置
- 首版支持拖拽导入

## Technical Approach

- 使用 `Python + tkinter + FFmpeg + ffprobe + PyInstaller`
- Python 负责 GUI、任务编排、参数校验、错误提示与打包入口
- `ffmpeg` 负责实际转码，`ffprobe` 负责输入探测
- 程序启动时优先使用程序内置的 `ffmpeg` / `ffprobe`
- 首版直接通过 `subprocess` 调用 `ffmpeg` / `ffprobe`
- 开发期优先产出 `one-folder`，稳定后再补 `one-file exe`
- 首版交付形态接受“解压文件夹后双击运行”
- 打包时将 `ffmpeg` / `ffprobe` 一并分发

## Decision (ADR-lite)

**Context**：项目从零开始，目标是最小成本落地 Windows 音频格式转换器，并最终导出可分发的 `exe`。

**Decision**：首版采用 `tkinter` 作为 GUI，采用 `FFmpeg` 作为转码引擎，采用 `PyInstaller` 进行打包，并内置 `ffmpeg` / `ffprobe`，优先服务完全不懂技术的普通用户。

**Consequences**：

- 优点是普通用户双击即可用，失败点更少，可迁移性更强
- 缺点是包体会明显变大，需要处理第三方二进制随包分发
- 需要补充 `FFmpeg` 许可证、来源说明和分发注意事项
- 若后续需要更现代界面，再评估 `customtkinter` 或其他桌面技术

## Implementation Plan

- Step 1 -> 验证标准：搭建项目骨架、依赖清单、FFmpeg 定位策略明确
- Step 2 -> 验证标准：完成单文件转换主流程，可成功输出目标格式文件
- Step 3 -> 验证标准：完成批量转换、输出目录选择、基础错误提示
- Step 4 -> 验证标准：完成 `tkinter` 最小 GUI，可选择文件、格式、目录并触发转换
- Step 5 -> 验证标准：完成 Windows `one-folder` 打包脚本/说明，能产出可分发目录
- Step 6 -> 验证标准：补充使用文档与分发注意事项，主流程自检通过

## Technical Notes

- 推荐方案：Python + GUI + FFmpeg + PyInstaller
- 已确认 GUI：`tkinter`
- 调研文件：`research/tech-options.md`
