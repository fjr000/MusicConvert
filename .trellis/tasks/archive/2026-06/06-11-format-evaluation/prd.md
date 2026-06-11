# 评测所有支持格式

## Goal

结合联网调研与本地执行，收集合规可用的音频测试样本，重点评测当前工具声明支持的加密输入格式到至少一种输出格式的转换表现；普通输入格式作为基线覆盖，最终形成可复查的评测结果与问题清单。

## What I already know

* 项目是 Windows 桌面音频格式转换工具，入口为 `python -m app.main`。
* 核心转换逻辑在 `app/converter.py`，格式声明在 `app/config.py`。
* 普通输入格式：`mp3` `wav` `flac` `m4a` `aac` `ogg` `opus` `wma`。
* 加密输入格式：`ncm` `tm2` `tm6` `qmc0` `qmc2` `qmc3` `qmc4` `qmc6` `qmc8` `qmcogg` `qmcflac` `tkm` `bkcmp3` `bkcm4a` `bkcwma` `bkcogg` `bkcwav` `bkcape` `bkcflac` `mgg` `mgg1` `mggl` `mflac` `mflac0` `mmp4` `6d7033` `6d3461` `6f6767` `776176` `666c6163` `kgm` `kgma` `vpr` `kwm` `x2m` `x3m` `xm`。
* 额外支持 `.qmc*` 前缀变种，如 `.qmc999`。
* 输出格式：`mp3` `wav` `flac` `m4a` `aac` `ogg` `opus`。
* 当前仓库已有三个 `.kgm` 样本文件，但没有完整覆盖所有加密格式。
* 自检命令：`python -m unittest discover -s tests`、`python -m compileall app tests` 已在只读理解阶段通过。

## Assumptions (temporary)

* 评测应优先使用公开、可合法下载或可本地生成的测试素材。
* 普通音频格式可通过公开样本或本地 ffmpeg 生成覆盖。
* 加密音频格式未必都有公开合法样本；无法取得样本的格式应在报告中标记为 `未覆盖：缺少合规样本`，而不是伪造成功。
* 测试样本和评测输出应放在临时/忽略目录中，避免把大文件提交进仓库。

## Open Questions

* 已确认：只使用公开可合法下载/生成/本地已有的测试样本；找不到合规样本的加密格式标记为 `未覆盖：缺少合规样本`。

## Requirements (evolving)

* 使用联网调研定位测试样本来源，优先一手/许可清晰来源。
* 评测重点为加密输入格式；普通输入格式仅作为转换链路基线覆盖。
* 下载或生成覆盖普通输入格式的样本。
* 尽量覆盖加密输入格式；样本缺失时记录原因。
* 对每个有样本的输入格式执行转换评测，记录成功/失败、失败原因、输出文件基本可用性。
* 产出一份中文评测报告，列出每个支持格式的覆盖状态。

## Acceptance Criteria (evolving)

* [ ] 有评测报告，逐项列出所有声明支持的输入格式。
* [ ] 每个格式都有状态：通过 / 失败 / 未覆盖（含原因）。
* [ ] 评测报告记录样本来源或生成方式。
* [ ] 不把下载的大型音频样本、转换输出提交到 Git。
* [ ] 项目原有单元测试和 compileall 保持通过。

## Definition of Done

* 评测报告已落盘到任务目录或项目文档位置。
* 测试样本来源、命令、结果可复查。
* 如发现代码缺陷，先汇报并确认是否进入修复范围。
* 如修改代码，必须完成 Trellis Phase 2/3 的实现、检查和提交流程。

## Out of Scope (explicit)

* 不绕过 DRM，不下载或传播明显侵权素材。
* 不承诺找到所有加密格式的真实样本。
* 未经确认不改动产品代码。
* 未经确认不提交大型二进制测试样本。

## Technical Notes

* 相关代码：`app/config.py`、`app/converter.py`、`app/decryptor.py`、`app/file_ops.py`。
* 相关测试：`tests/test_converter.py`、`tests/test_decryptor.py`、`tests/test_file_ops.py`。
* 联网操作需通过 `web-access` skill；已检查 Node/Chrome/CDP Proxy 可用。
