# 代码架构文档

## 项目结构

```
MusicConvert/
├── app/                    # 主应用代码
│   ├── config.py          # 配置常量（支持的格式列表）
│   ├── models.py          # 数据模型（SourceItem, ConvertResult）
│   ├── ffmpeg_tools.py    # 工具路径查找逻辑
│   ├── decryptor.py       # 加密音频解密模块
│   ├── converter.py       # 音频格式转换核心逻辑
│   ├── file_ops.py        # 文件收集和路径处理
│   ├── gui.py             # tkinter GUI 界面
│   ├── main.py            # 程序入口
│   └── kgm.py             # [已弃用] KGM 格式包装器
├── tests/                  # 单元测试
│   ├── test_converter.py
│   ├── test_decryptor.py
│   ├── test_file_ops.py
│   └── test_encrypted_formats.py
├── tools/                  # 外部工具二进制
│   ├── ffmpeg/
│   │   ├── ffmpeg.exe
│   │   └── ffprobe.exe
│   └── musicdecrypto/
│       ├── musicdecrypto.exe
│       └── THIRD_PARTY.md
└── docs/                   # 文档
    └── ENCRYPTION_RESEARCH.md

## 模块职责

### config.py
定义支持的音频格式常量：
- `SUPPORTED_AUDIO_INPUT_FORMATS`: 普通音频格式
- `SUPPORTED_ENCRYPTED_INPUT_FORMATS`: 加密音频格式
- `ENCRYPTED_AUDIO_PREFIXES`: 加密格式前缀（如 `.qmc*`）
- `SUPPORTED_OUTPUT_FORMATS`: 支持的输出格式

### models.py
数据传输对象：
- `SourceItem`: 源文件路径 + 相对路径
- `ConvertResult`: 转换结果（成功/失败 + 消息）

### ffmpeg_tools.py
工具路径解析：
- `get_runtime_root()`: 获取运行时根目录（支持 PyInstaller）
- `get_tool_path()`: 查找工具路径（bundled > local > PATH）
- `get_ffmpeg_path()`, `get_ffprobe_path()`, `get_musicdecrypto_path()`

### decryptor.py
加密音频处理：
- `is_encrypted_audio_file()`: 检测是否为加密格式
- `build_decrypt_command()`: 构建解密命令
- `decrypt_audio_to_temp()`: 解密到临时目录
- `cleanup_decrypted_path()`: 清理临时文件（处理 Windows 文件锁）

### converter.py
转换核心逻辑：
- `probe_audio()`: 使用 ffprobe 验证音频流
- `build_ffmpeg_command()`: 构建 ffmpeg 转换命令
- `convert_one()`: 单文件转换（处理加密 + 转换）
- `convert_many()`: 批量转换

### file_ops.py
文件系统操作：
- `is_supported_input()`: 检查文件是否支持
- `collect_file_items()`: 从文件列表收集项目
- `collect_folder_items()`: 递归收集文件夹中的音频文件
- `build_output_path()`: 构建输出路径（保留目录结构）
- `make_unique_path()`: 生成唯一路径（避免重名）

### gui.py
GUI 界面：
- `App`: 主应用窗口类
  - 支持拖放文件/文件夹
  - 格式选择和输出目录配置
  - 实时显示转换进度和结果
  - 使用 tkinterdnd2 实现拖放功能

### kgm.py (已弃用)
历史遗留的 KGM 格式包装器，现在直接使用 `decryptor.py` 中的通用函数。保留是为了向后兼容，但已标记为 DEPRECATED。

## 数据流

```
用户选择文件/文件夹
    ↓
file_ops.collect_file_items() / collect_folder_items()
    ↓
生成 SourceItem 列表
    ↓
converter.convert_many()
    ↓
对每个文件：converter.convert_one()
    ↓
    ├─ 检测是否加密 (decryptor.is_encrypted_audio_file)
    ├─ 如果加密 → decryptor.decrypt_audio_to_temp()
    ├─ 验证音频流 (converter.probe_audio)
    ├─ ffmpeg 转换
    └─ 清理临时文件 (decryptor.cleanup_decrypted_path)
    ↓
返回 ConvertResult 列表
    ↓
GUI 显示结果
```

## 错误处理策略

1. **文件级隔离**: 单个文件失败不影响批处理其他文件
2. **用户友好提示**: 捕获技术错误，转换为简短中文提示
3. **资源清理**: 使用 try-finally 确保临时文件清理
4. **Windows 特殊处理**: 文件锁重试机制（5次，间隔 0.2s）

## 测试覆盖

- **单元测试**: 测试各模块核心函数
- **集成测试**: 测试完整转换流程
- **格式测试**: 验证所有支持格式的检测逻辑
- **边界测试**: 文件不存在、格式不支持、路径冲突等

## PyInstaller 打包

使用 `music_converter.spec` 配置：
- 单文件夹模式 (one-folder)
- 打包 `tools/` 目录下的所有工具
- 输出到 `dist/音乐格式转换器/`

## 代码风格

- Python 3.10+ 类型注解
- Pathlib 替代字符串路径
- Dataclass 替代 dict
- 函数文档字符串（关键函数）
- 中文错误提示（用户可见）
- 英文代码注释（开发者可见）
