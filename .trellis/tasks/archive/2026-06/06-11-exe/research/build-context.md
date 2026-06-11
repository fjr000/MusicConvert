# 导出 exe 构建上下文

## 用户确认

- 用户已确认由助手补齐缺失的 `ffmpeg.exe` / `ffprobe.exe` 后再打包。

## 仓库事实

- `README.md` 说明打包命令为 `pyinstaller music_converter.spec`。
- `music_converter.spec` 是 one-folder 构建，输出名为 `音乐格式转换器`。
- `music_converter.spec` 会把当前存在的 `tools/ffmpeg` 与 `tools/musicdecrypto` 目录加入 PyInstaller datas。
- 当前已有 `tools/musicdecrypto/musicdecrypto.exe`。
- 需要补齐 `tools/ffmpeg/ffmpeg.exe` 与 `tools/ffmpeg/ffprobe.exe`。

## FFmpeg 获取方案

- 使用 BtbN FFmpeg Windows LGPL 构建：`https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-lgpl.zip`。
- 只从压缩包中提取 `bin/ffmpeg.exe` 与 `bin/ffprobe.exe` 到 `tools/ffmpeg/`。
- 补充 `tools/ffmpeg/THIRD_PARTY.md` 记录来源与许可证提示。

## 构建与验收

- 安装依赖：`python -m pip install -r requirements.txt`（如缺少 PyInstaller）。
- 打包：`python -m PyInstaller music_converter.spec` 或 `pyinstaller music_converter.spec`。
- 验收：确认 `dist/音乐格式转换器/音乐格式转换器.exe` 存在，并确认 `dist/音乐格式转换器/tools/ffmpeg/ffmpeg.exe` 与 `ffprobe.exe` 存在。
