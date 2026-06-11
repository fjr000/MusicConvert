# KGM 方案调研

## 结论

本项目优先采用“外部开源解密器 + 现有 FFmpeg 转换流程复用”的路线。

原因：
- 当前仓库是 Python + Tkinter + 外部 `ffmpeg/ffprobe` 的最小桌面工具。
- 公开可见的 KGM 方案主要是独立 CLI/桌面程序，几乎没有成熟的 Python 包可直接引入。
- 继续沿用“Python 调外部工具”的模式，改动最小。

## 候选方案观察

### MusicDecrypto
- 仓库：`davidxuang/MusicDecrypto`
- 形态：`.NET` 库 + CLI
- README 明示支持 KGM 系列格式。
- 许可证：核心库 `LGPL-2.1`，CLI/GUI `AGPL-3.0`。
- 影响：若直接复用 CLI，需要谨慎处理 AGPL 分发义务；若仅参考其支持范围，说明 KGM 离线解密具备可行性。

### AudioDecrypt
- 仓库：`0x77fe/AudioDecrypt`
- 形态：独立桌面工具
- README 提到其解密思路基于 `unlock-music`。
- 许可证：GitHub API 返回 `GPL-3.0`。
- 影响：可作为“已有 KGM 解密实践”的旁证，但维护状态一般，不优先直接集成。

### Kugo-Music-Converter
- 仓库：`skxxxkx666/Kugo-Music-Converter`
- 形态：Go 后端 + 本地 Web UI + 外部 ffmpeg
- README 明示支持 `.kgm` 转普通音频。
- 许可证：`GPL-3.0`。
- 影响：架构上与本项目“本地工具 + 外部转码器”接近，证明路线可行；但仍不是 Python 依赖。

## 对本任务的直接约束

- 不假设存在可 `pip install` 的 KGM Python 库。
- 需要为 KGM 增加“前置解密”步骤，再进入现有 `ffprobe` / `ffmpeg` 流程。
- 解密器应支持离线运行。
- 失败时应返回简短、可读的错误文案，不展示原始整段日志。
- 中间解密产物默认使用临时文件，转换完成后删除。

## 待实现时重点验证

- 最终选中的解密器是否能在当前 Windows 打包方式下随程序分发。
- 三个样本 `.kgm` 是否都能成功解出普通音频。
- 解出的临时文件扩展名/真实格式是否会影响 `ffprobe` 识别。
- 分发时是否需要补充第三方工具许可证与来源说明。
