# 音乐格式转换器

一个面向 Windows 的最小可用音乐格式转换工具。

## 功能

- 单文件转换
- 批量文件转换
- 整文件夹递归扫描音频文件
- 保留文件夹相对目录结构输出
- 输出重名时自动重命名
- 顺序执行，单文件失败不中断整批
- 优先使用内置 `ffmpeg.exe` / `ffprobe.exe`

## 支持格式

### 输入

`mp3` `wav` `flac` `m4a` `aac` `ogg` `opus` `wma`

### 输出

`mp3` `wav` `flac` `m4a` `aac` `ogg` `opus`

## 开发运行

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python -m app.main
```

## FFmpeg 放置方式

开发和打包时都优先从以下位置查找：

- `tools/ffmpeg/ffmpeg.exe`
- `tools/ffmpeg/ffprobe.exe`

如果是 PyInstaller 打包后的目录运行，也会优先从程序解包目录中的 `tools/ffmpeg/` 查找。

## 打包 one-folder

先准备：

- Windows 环境
- 可运行的 Python 3
- `tools/ffmpeg/ffmpeg.exe`
- `tools/ffmpeg/ffprobe.exe`

执行：

```bash
pyinstaller music_converter.spec
```

输出目录：`dist/音乐格式转换器/`

## 分发注意事项

- 首版目标是 Windows 便携版，不承诺跨平台
- 请随程序一起分发 `ffmpeg` / `ffprobe` 二进制
- 请补充 FFmpeg 来源、许可证文本和对应说明
- 不承诺支持冷门、私有或 DRM 音频格式

## 自检

```bash
python -m unittest discover -s tests
python -m compileall app tests
```
