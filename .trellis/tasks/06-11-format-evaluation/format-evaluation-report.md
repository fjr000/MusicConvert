# 支持格式转换评测报告

评测日期：2026-06-11  
任务：`.trellis/tasks/06-11-format-evaluation`  
入口：直接调用 `app.converter.convert_one(...)`，每个有样本的输入格式转换到至少一种输出格式后再用 `ffprobe` 验证输出是否含音频流。

## 1. 结论摘要

- 普通输入格式基线：`mp3`、`wav`、`flac`、`m4a`、`aac`、`ogg`、`opus`、`wma` 全部通过。样本均由本机 `ffmpeg` 生成 1 秒正弦音频，转换输出可被 `ffprobe` 识别为音频。
- 合规公开加密样本：从 `Huibq/parakeet-crypto-rs` 下载并评测了 `.kgm` 三个版本、`.qmcogg`、`.mgg` 三种、`.x2m`、`.x3m`。这些公开样本在当前工具链下全部失败，产品返回 `解密失败，请检查文件是否受支持`，未生成可验证输出。
- 本地已有 `.kgm` 三个样本可成功转换到 `mp3`，但来源/授权未核实，不能作为合规公开覆盖证据，只作为辅助诊断：当前工具并非完全不能处理 `.kgm`，而是不能处理本次找到的公开 KGM 测试样本变种。
- 其他声明的加密扩展名未找到许可清晰、可复查的公开完整样本，按任务约定标记为 `未覆盖：缺少合规样本`，不伪造成功。

## 2. 临时目录与 Git 风险控制

- 临时样本、转换输出、原始日志目录：`.trellis/tasks/06-11-format-evaluation/scratch/`
- 已创建忽略文件：`.trellis/tasks/06-11-format-evaluation/scratch/.gitignore`

`.gitignore` 内容：

```gitignore
*
!.gitignore
```

因此下载样本、生成音频、转换输出和原始 JSON/TSV 日志均不会进入 Git；本报告只记录可复查的来源、hash、命令和结论。

## 3. 环境与工具可用性

| 工具 | 检查结果 | 备注 |
|---|---:|---|
| web-access 前置检查 | 通过 | `node .../web-access/scripts/check-deps.mjs`：Node v24.11.1，Chrome port 10073，proxy ready。 |
| `ffmpeg` | 可用 | `ffmpeg version 7.1-full_build-www.gyan.dev`；项目路径解析回退到 `ffmpeg.exe`，由 PATH 解析到本机安装。 |
| `ffprobe` | 可用 | `ffprobe version 7.1-full_build-www.gyan.dev`；由 PATH 解析到本机安装。 |
| `musicdecrypto.exe` | 可执行 | `tools/musicdecrypto/musicdecrypto.exe` 存在；无参数运行显示 USAGE。 |

## 4. 公开加密样本清单

来源仓库：`https://github.com/Huibq/parakeet-crypto-rs`  
样本目录 API：`https://api.github.com/repos/Huibq/parakeet-crypto-rs/contents/sample?ref=main`  
样本说明：`https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/README.MD`

| 文件 | 大小 byte | SHA-256 | URL |
|---|---:|---|---|
| `test_kgm_v2.kgm` | 36036 | `93b6b12394e4a03f7a5aa80355cc24b0e82e46c1040363a740c759cb3d07ead5` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v2.kgm |
| `test_kgm_v3.kgm` | 36036 | `85f30d7d8a362ddbe0140bc7539ca7a60344578b76e181516505c657b1f86791` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v3.kgm |
| `test_kgm_v4.kgm` | 36036 | `7be529505d65687d2a7e8853eb327d911ed758cfdca672927a1e58fff523822e` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v4.kgm |
| `test_qmc1.qmcogg` | 35012 | `b6c97c9de704a88fd45822437a763d4971f9fac5fdabf6a432bd1b98228e69d2` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc1.qmcogg |
| `test_qmc2_map.mgg` | 35380 | `49c4307522ae66b3a14a0e526f9fd29bd7a744edd1067945bef8fbd33789c7f5` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc2_map.mgg |
| `test_qmc2_rc4.mgg` | 35720 | `ab42096669c32625ce22755af7a65a37b67a0f21f3b0080c9ad9f0cd400bf162` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc2_rc4.mgg |
| `test_qmc2_rc4_EncV2.mgg` | 36024 | `9b508551d81b535d37403bcc5cd8ccac5fe06b8943d30356726eb4ea82c09b92` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc2_rc4_EncV2.mgg |
| `test_xmly.x2m` | 35012 | `4bb07751b23b09920854985a98e9166233b06be299ce639fa99fe1403cb68e44` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_xmly.x2m |
| `test_xmly.x3m` | 35012 | `d81279fe73fd103660373a7bdf6fcf4682fbee52239f340c2b193c920cb2f603` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_xmly.x3m |
| `test_x2m_key.bin` | 4 | `eccb7c0c8da7b9937419918fd8a191d0f25a750aff1b9df401bca0904bf59d63` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_x2m_key.bin |
| `test_x3m_key.bin` | 32 | `0d2cd57a03ad7526cfedf61eca3ace05450c5410436c20aa4f23400ba1abcb17` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_x3m_key.bin |
| `test_xmly_scramble_table.bin` | 2048 | `65b58b1439354e79e78d8a2e155455813b87736987c6af8b8855216c28b3e0e1` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_xmly_scramble_table.bin |
| `kgm_header_v2.bin` | 64 | `46d2d45b067a8de39c863b7e32e9587cc1b4644501292cd60019e5e05e06faf9` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/kgm_header_v2.bin |
| `kgm_header_v3.bin` | 64 | `873d26b52199d5d94d08a0ee1d98156a971d8b58cb86dbf09acde2981683f4f9` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/kgm_header_v3.bin |
| `kgm_header_v4.bin` | 64 | `4ed55d986f6efdc8cdd8cdfc11ceca320db0e8052ed056177c867e08e8d86835` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/kgm_header_v4.bin |
| `test_kgm_v4_filekey_table.bin` | 705 | `5c03932796b7855b3cea772dd3a9a6097ac5eba774a6847fd5a2d73628576eaf` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v4_filekey_table.bin |
| `test_kgm_v4_slotkey_table.bin` | 712 | `e248e329dbee4dbf453fe53481f52334fedc2a75050abdb30bad3ed453d6a30f` | https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v4_slotkey_table.bin |

## 5. 普通输入格式基线结果

生成方式：`ffmpeg -f lavfi -i sine=frequency=440:duration=1 ...`。  
转换方式：除 `wav` 转 `mp3` 外，其余普通输入均转 `wav`。输出均通过 `ffprobe` 检测到音频流。

普通基线样本 SHA-256：

| 文件 | 大小 byte | SHA-256 |
|---|---:|---|
| `baseline.mp3` | 8585 | `8fa28f712562f6fc4b82cd0e261ae12dd80bb573a2be4ca1e74406630103a498` |
| `baseline.wav` | 88278 | `76d884aeb068036704cf27022000c5e91b739ac17d6b1ce27ba61ddda870d706` |
| `baseline.flac` | 20333 | `6605320cc3c64f0478fea14f24117dac80186571c921c41d01a526eab24e9187` |
| `baseline.m4a` | 9969 | `f66e5fb8c074748f65de57da4afd9e94794c3f4ee8a90f768d78d0014208945f` |
| `baseline.aac` | 9298 | `85a32adaaaef4dfa1dff01bb07a6ffe54bb4daf5b437045dd27e4715a3f2b5ca` |
| `baseline.ogg` | 5264 | `495099c9bccf07341acf5fb975322bfc0196b995a50c51c460f9461933e74bb2` |
| `baseline.opus` | 9396 | `93834bf56e39508f0feee604bc346a53e8f369b6da4c36b847f61be4277c1dec` |
| `baseline.wma` | 19742 | `f0b4db9032428cf278f5cc62979f41ddb8f9940046ed905580cf786e2fb37b56` |

| 输入格式 | 样本生成 | 转换目标 | 状态 | 输出验证 |
|---|---|---|---|---|
| `mp3` | `libmp3lame` 生成 1 秒正弦音 | `wav` | 通过 | `pcm_s16le`，约 1.000s |
| `wav` | `pcm_s16le` 生成 1 秒正弦音 | `mp3` | 通过 | `mp3`，约 1.045s |
| `flac` | `flac` 生成 1 秒正弦音 | `wav` | 通过 | `pcm_s16le`，约 1.000s |
| `m4a` | `aac` in M4A 生成 1 秒正弦音 | `wav` | 通过 | `pcm_s16le`，约 1.022s |
| `aac` | `aac` ADTS 生成 1 秒正弦音 | `wav` | 通过 | `pcm_s16le`，约 1.045s |
| `ogg` | `libvorbis` 生成 1 秒正弦音 | `wav` | 通过 | `pcm_s16le`，约 0.997s |
| `opus` | `libopus` 生成 1 秒正弦音 | `wav` | 通过 | `pcm_s16le`，约 1.000s |
| `wma` | `wmav2` 生成 1 秒正弦音 | `wav` | 通过 | `pcm_s16le`，约 0.975s |

## 6. 加密输入格式逐项结果

| 输入格式 | 状态 | 样本/来源 | 转换目标 | 结果说明 |
|---|---|---|---|---|
| `ncm` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `tm2` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `tm6` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `qmc0` | 未覆盖 | MusicDecrypto 有算法片段，非完整容器 | - | 不作为端到端输入样本。 |
| `qmc2` | 未覆盖 | 未找到该扩展名合规公开完整样本 | - | `.mgg` 另行评测，不能替代 `.qmc2` 扩展名覆盖。 |
| `qmc3` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `qmc4` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `qmc6` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `qmc8` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `qmcogg` | 失败 | `parakeet-crypto-rs/sample/test_qmc1.qmcogg` | `mp3` | `convert_one` 返回 `解密失败，请检查文件是否受支持`；无输出文件。 |
| `qmcflac` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `tkm` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `bkcmp3` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `bkcm4a` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `bkcwma` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `bkcogg` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `bkcwav` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `bkcape` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `bkcflac` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `mgg` | 失败 | `test_qmc2_map.mgg`、`test_qmc2_rc4.mgg`、`test_qmc2_rc4_EncV2.mgg` | `mp3` | 三个公开样本均返回 `解密失败，请检查文件是否受支持`；无输出文件。 |
| `mgg1` | 未覆盖 | 未找到该扩展名合规公开完整样本 | - | 缺少合规样本。 |
| `mggl` | 未覆盖 | 未找到该扩展名合规公开完整样本 | - | 缺少合规样本。 |
| `mflac` | 未覆盖 | MusicDecrypto 有算法片段，非完整容器 | - | 不作为端到端输入样本。 |
| `mflac0` | 未覆盖 | MusicDecrypto 有算法片段，非完整容器 | - | 不作为端到端输入样本。 |
| `mmp4` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `6d7033` | 未覆盖 | 未找到合规公开完整样本 | - | QMC 十六进制后缀；缺少合规样本。 |
| `6d3461` | 未覆盖 | 未找到合规公开完整样本 | - | QMC 十六进制后缀；缺少合规样本。 |
| `6f6767` | 未覆盖 | 未找到合规公开完整样本 | - | QMC 十六进制后缀；缺少合规样本。 |
| `776176` | 未覆盖 | 未找到合规公开完整样本 | - | QMC 十六进制后缀；缺少合规样本。 |
| `666c6163` | 未覆盖 | 未找到合规公开完整样本 | - | QMC 十六进制后缀；缺少合规样本。 |
| `kgm` | 失败 | `test_kgm_v2.kgm`、`test_kgm_v3.kgm`、`test_kgm_v4.kgm` | `mp3` | 三个合规公开样本均返回 `解密失败，请检查文件是否受支持`；无输出文件。本地已有 `.kgm` 三个样本辅助测试通过，但不作为合规覆盖证据。 |
| `kgma` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `vpr` | 未覆盖 | 未找到完整容器样本 | - | parakeet 仓库可见 VPR 相关测试向量线索，但未找到可直接端到端转换的 `.vpr` 样本。 |
| `kwm` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `x2m` | 失败 | `parakeet-crypto-rs/sample/test_xmly.x2m`，已下载配套 key/table | `mp3` | `convert_one` 返回 `解密失败，请检查文件是否受支持`；无输出文件。 |
| `x3m` | 失败 | `parakeet-crypto-rs/sample/test_xmly.x3m`，已下载配套 key/table | `mp3` | `convert_one` 返回 `解密失败，请检查文件是否受支持`；无输出文件。 |
| `xm` | 未覆盖 | 未找到合规公开完整样本 | - | 缺少合规样本。 |
| `.qmc*` 前缀变种 | 部分覆盖/失败 | `.qmcogg` 触发了 qmc 前缀分支；未找到 `.qmc999` 这类合规公开样本 | `mp3` | `.qmcogg` 样本解密失败；其他前缀变种未覆盖。 |

## 7. 本地已有 KGM 辅助结果（非合规公开样本）

这些文件位于仓库根目录，来源/授权未核实，不应复制或传播，仅用于判断当前解密链路是否完全不可用。

| 本地文件 | 大小 byte | SHA-256 | 状态 | 输出验证 |
|---|---:|---|---|---|
| `Lost Frequencies、Janieck - Reality.kgm` | 2554180 | `3ead52c38a6f8cb4bf734ec6aca1d114180a76c748b28ceb47ab6bcd0cf29c07` | 通过 | 转 `mp3` 成功，`ffprobe` 检测到 `mp3`，约 159.530s。 |
| `徐梦圆 - China-X.kgm` | 3618668 | `aaf845c3a21b9c8380adf0a891d9311ef131c43ab9d6289ab9f9b4b7ec2312a6` | 通过 | 转 `mp3` 成功，`ffprobe` 检测到 `mp3`，约 226.064s。 |
| `越人歌 (钢琴伴奏).kgm` | 8641038 | `cbce2ca3f695a9fdac4f8eac10d1c1883e5d184c8cd2a183f807117e2cb173a8` | 通过 | 转 `mp3` 成功，`ffprobe` 检测到 `mp3`，约 211.252s。 |

## 8. 复查命令摘要

### 8.1 下载公开样本

```bash
mkdir -p .trellis/tasks/06-11-format-evaluation/scratch/encrypted-samples
cd .trellis/tasks/06-11-format-evaluation/scratch/encrypted-samples
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v2.kgm
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v3.kgm
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v4.kgm
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc1.qmcogg
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc2_map.mgg
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc2_rc4.mgg
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc2_rc4_EncV2.mgg
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_xmly.x2m
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_xmly.x3m
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_x2m_key.bin
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_x3m_key.bin
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_xmly_scramble_table.bin
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/kgm_header_v2.bin
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/kgm_header_v3.bin
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/kgm_header_v4.bin
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v4_filekey_table.bin
curl -L --fail -O https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v4_slotkey_table.bin
sha256sum *
```

### 8.2 生成普通基线样本示例

```bash
ffmpeg.exe -y -f lavfi -i sine=frequency=440:duration=1 -c:a libmp3lame scratch/plain-samples/baseline.mp3
ffmpeg.exe -y -f lavfi -i sine=frequency=440:duration=1 -c:a pcm_s16le scratch/plain-samples/baseline.wav
ffmpeg.exe -y -f lavfi -i sine=frequency=440:duration=1 -c:a flac scratch/plain-samples/baseline.flac
ffmpeg.exe -y -f lavfi -i sine=frequency=440:duration=1 -c:a aac scratch/plain-samples/baseline.m4a
ffmpeg.exe -y -f lavfi -i sine=frequency=440:duration=1 -c:a aac -f adts scratch/plain-samples/baseline.aac
ffmpeg.exe -y -f lavfi -i sine=frequency=440:duration=1 -c:a libvorbis scratch/plain-samples/baseline.ogg
ffmpeg.exe -y -f lavfi -i sine=frequency=440:duration=1 -c:a libopus scratch/plain-samples/baseline.opus
ffmpeg.exe -y -f lavfi -i sine=frequency=440:duration=1 -c:a wmav2 scratch/plain-samples/baseline.wma
sha256sum scratch/plain-samples/*
```

### 8.3 转换与输出验证逻辑

```python
from pathlib import Path
from app.converter import convert_one

result = convert_one(Path("input.ext"), Path("output.mp3"), "mp3")
print(result.success, result.message)
```

输出基本可用性验证：

```bash
ffprobe.exe -v error -show_entries stream=codec_type,codec_name:format=duration -of json output.mp3
```

## 9. 问题清单与建议

1. 公开合规加密样本覆盖到的 `kgm`、`qmcogg`、`mgg`、`x2m`、`x3m` 当前全部失败，需确认产品声明是否应细化为“部分变种支持”。
2. `musicdecrypto.exe` 对失败样本会打印 `Decryption has failed`，部分诊断中还出现 `NotImplementedException`，但进程退出码仍为 0；当前产品依赖“是否生成唯一输出文件”判断失败，因此最终用户结果仍为失败，但诊断信息会被压缩成通用中文错误。
3. `x2m` / `x3m` 公开样本附带 key/table；当前产品解密流程会把源文件复制到临时目录后调用 CLI，没有复制或传递配套 key/table。直接把 key/table 与样本放在同目录调用 CLI 仍未成功，但如果未来确认某些格式必须使用 sidecar 文件，需要先设计产品输入模型再修复。
4. 本地 `.kgm` 辅助样本通过，公开 KGM v2/v3/v4 样本失败，说明 KGM 支持范围依赖具体变种/实现，建议后续单独确认 KGM 版本矩阵。

本次任务未修改 `app/`、`tests/` 或打包配置。若要修复加密格式兼容性，需要另起修复范围并确认预期支持的加密变种与样本来源。
