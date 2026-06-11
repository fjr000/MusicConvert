# 导出 exe

## 目标

将当前音乐格式转换器项目按现有 PyInstaller 配置打包为 Windows one-folder 可执行程序，输出到 `dist/音乐格式转换器/`，便于本机运行或分发。

## 已知信息

- 用户要求：导出 exe。
- 项目已有 PyInstaller 配置：`music_converter.spec`。
- README 已给出打包命令：`pyinstaller music_converter.spec`。
- 输出目录约定为：`dist/音乐格式转换器/`。
- 当前仓库存在 `tools/musicdecrypto/musicdecrypto.exe`。
- 当前仓库未发现 `tools/ffmpeg/ffmpeg.exe` 和 `tools/ffmpeg/ffprobe.exe`。
- `music_converter.spec` 只会打包当前实际存在的 `tools/ffmpeg` 与 `tools/musicdecrypto` 目录。

## 临时假设

- 本次只按现有配置打包，不修改应用代码。
- 目标平台是 Windows。
- 用户已确认由助手补齐缺失的 `ffmpeg.exe` / `ffprobe.exe` 后再打包。
- 首轮打包后检查发现当前 `app/gui.py` 缺少 `start_convert` 方法，exe 虽生成但 GUI 可能无法启动，需要做最小阻塞修复后重新打包。

## 待确认问题

- 无。

## 需求（演进中）

- 补齐 `tools/ffmpeg/ffmpeg.exe` 与 `tools/ffmpeg/ffprobe.exe`。
- 如当前代码存在阻止 exe 启动的明显问题，只做最小必要修复。
- 使用现有 PyInstaller spec 导出 exe。
- 尽量不改应用代码和打包配置；若必须修复启动阻塞，只改直接相关位置。
- 打包后确认输出目录存在。

## 验收标准（演进中）

- [x] `tools/ffmpeg/ffmpeg.exe` 与 `tools/ffmpeg/ffprobe.exe` 存在。
- [x] GUI 初始化不再因缺少 `start_convert` 方法失败。
- [x] 打包命令执行完成。
- [x] `dist/音乐格式转换器/音乐格式转换器.exe` 存在。
- [x] `dist/音乐格式转换器/_internal/tools/ffmpeg/ffmpeg.exe` 与 `dist/音乐格式转换器/_internal/tools/ffmpeg/ffprobe.exe` 存在。

## 完成定义

- 打包输出已生成，或明确说明阻塞原因。
- 如执行了命令，记录关键结果。
- 不引入不必要代码变更。

## 范围外

- 不下载或替换除 FFmpeg/FFprobe 以外的第三方工具。
- 不修改 GUI、转换逻辑或加密音频支持逻辑。
- 不承诺跨平台构建。

## 技术备注

- 已检查 `README.md`：存在打包说明和分发注意事项。
- 已检查 `music_converter.spec`：one-folder 打包，`console=False`，名称为 `音乐格式转换器`。
- 已检查 `requirements.txt`：依赖 `pyinstaller>=6.0`。
- 已检查 `tools/`：仅发现 `tools/musicdecrypto/musicdecrypto.exe`。
- FFmpeg 获取方案记录在 `research/build-context.md`。
- 已执行 `.venv/Scripts/python.exe -m PyInstaller -y music_converter.spec` 并通过检查。
- 已执行 `.venv/Scripts/python.exe -m unittest discover -s tests`：29 个测试通过。
- 已执行 `.venv/Scripts/python.exe -m compileall -q app tests`：通过。
