# 音乐格式转换器

一个面向 Windows 的音乐格式转换工具，支持常见音频格式和主流加密音频格式。

## 功能特性

- ✅ 单文件 / 批量文件转换
- 📁 文件夹递归扫描音频文件
- 🎯 保留文件夹相对目录结构输出
- 🔄 输出重名时自动重命名
- 🎨 现代化 GUI 界面，支持拖放操作
- 🛡️ 顺序执行，单文件失败不中断整批
- 🔧 优先使用内置 `ffmpeg.exe` / `ffprobe.exe`
- 🔐 本地离线解密，保护隐私

## 支持格式

### 输入

普通音频：`mp3` `wav` `flac` `m4a` `aac` `ogg` `opus` `wma`

加密音频：`ncm` `tm2` `tm6` `qmc0` `qmc2` `qmc3` `qmc4` `qmc6` `qmc8` `qmcogg` `qmcflac` `tkm` `bkcmp3` `bkcm4a` `bkcwma` `bkcogg` `bkcwav` `bkcape` `bkcflac` `mgg` `mgg1` `mggl` `mflac` `mflac0` `mmp4` `6d7033` `6d3461` `6f6767` `776176` `666c6163` `kgm` `kgma` `vpr` `kwm` `x2m` `x3m` `xm`

说明：
- ✅ 额外识别 `qmc*` 前缀变种，例如 `.qmc999`，并按上游 CLI 的扩展检测模式处理
- ℹ️ 与普通音频重名的加密后缀（如普通 `.mp3` / `.flac`）首版不额外探测
- ⚠️ `mgg` / `mflac` 系列按上游工具说明仅做首版接入，个别样本可能仍会失败
- 🔐 所有加密格式均通过 `MusicDecrypto` 工具进行本地离线解密

### 输出

`mp3` `wav` `flac` `m4a` `aac` `ogg` `opus`

## 开发运行

### 安装依赖

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 运行程序

```bash
python -m app.main
```

### 运行测试

```bash
python -m unittest discover -s tests
python -m compileall app tests
```

## 工具放置方式

开发和打包时都优先从以下位置查找：

- `tools/ffmpeg/ffmpeg.exe`
- `tools/ffmpeg/ffprobe.exe`
- `tools/musicdecrypto/musicdecrypto.exe`

如果是 PyInstaller 打包后的目录运行，也会优先从程序解包目录中的对应 `tools/` 子目录查找。

## 打包 one-folder

先准备：

- Windows 环境
- 可运行的 Python 3
- `tools/ffmpeg/ffmpeg.exe`
- `tools/ffmpeg/ffprobe.exe`
- `tools/musicdecrypto/musicdecrypto.exe`（Windows x64 CLI）

执行：

```bash
pyinstaller music_converter.spec
```

输出目录：`dist/音乐格式转换器/`

## 分发注意事项

- ⚠️ 首版目标是 Windows 便携版，不承诺跨平台
- 📦 请随程序一起分发 `ffmpeg` / `ffprobe` 二进制
- 🔐 请随程序一起分发 `MusicDecrypto` 的 Windows x64 CLI
- 📄 请补充第三方工具来源、许可证文本和对应说明
  - `MusicDecrypto` 说明见 `tools/musicdecrypto/THIRD_PARTY.md`
  - 加密音频方案调研见 `docs/ENCRYPTION_RESEARCH.md`
- 🔒 加密音频会先调用 `MusicDecrypto` 做本地离线解密，再进入现有转换流程
- ✅ 某个加密文件解密失败时只影响当前文件，不中断整批
- 💬 用户侧失败提示保持简短中文，不展示底层长日志或堆栈
- ⚠️ 不承诺支持冷门、私有或 DRM 音频格式

## 自检

```bash
python -m unittest discover -s tests
python -m compileall app tests
```
