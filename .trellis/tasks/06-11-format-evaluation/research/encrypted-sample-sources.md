# 加密音频测试样本来源调研

调研日期：2026-06-11

## 结论摘要

目前找到的合规、公开、可直接下载并适合本项目端到端评测的样本主要来自 `parakeet-crypto-rs` 的 `sample/` 目录，可覆盖 `.kgm`、`.qmcogg`、`.mgg`、`.x2m`、`.x3m`。MusicDecrypto 上游仓库提供了算法测试数据片段，可覆盖部分 QMC/MGG/MFLAC 算法路径，但不是完整音频容器，不建议直接作为本项目端到端转换样本。其余多数加密扩展名未找到许可清晰、可复查的公开完整样本。

## 一手来源 1：MusicDecrypto 上游仓库

- 来源 URL：
  - 仓库：https://github.com/davidxuang/MusicDecrypto
  - README：https://raw.githubusercontent.com/davidxuang/MusicDecrypto/master/README.md
  - 支持格式表：https://raw.githubusercontent.com/davidxuang/MusicDecrypto/master/MusicDecrypto.Library/DecryptoFactory.cs
  - 测试数据目录 API：https://api.github.com/repos/davidxuang/MusicDecrypto/contents/MusicDecrypto.Library.Tests/DataSets?ref=master
  - 测试代码：https://raw.githubusercontent.com/davidxuang/MusicDecrypto/master/MusicDecrypto.Library.Tests/TencentTests.cs
- 可覆盖格式：
  - 完整容器样本：未发现。
  - 算法片段/测试向量：`qmc0`、`mgg`、`mflac`、`mflac0`。
  - 具体数据：`qmc0-static.payload(.enc)`、`mgg-map.*`、`mflac-map.*`、`mflac-rc4.*`、`mflac0-rc4.*`、`mflac_v2-map.*`。
- 许可/合规判断：
  - 仓库公开；GitHub API 标记仓库许可证为 AGPL-3.0。
  - README 声明核心库为 LGPL-2.1，CLI/GUI 为 AGPL-3.0。
  - `MusicDecrypto.Library.Tests/LICENSE` 是 LGPL-3.0 文本。
  - 数据是上游公开测试资源，但文件名与测试代码显示其用途是算法单元测试片段，不是完整歌曲或完整可播放容器。
- 可下载性：
  - 可通过 `raw.githubusercontent.com` 直接下载单个测试数据文件。
- 对本项目评测的建议：
  - 不作为本项目「输入文件 -> 输出音频」端到端转换样本。
  - 可作为后续补充的低层算法回归素材，但本项目当前依赖 `musicdecrypto.exe`，不是直接调用上游库内部算法，因此价值有限。

## 一手来源 2：parakeet-crypto-rs 样本目录

- 来源 URL：
  - 仓库：https://github.com/Huibq/parakeet-crypto-rs
  - README：https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/README.md
  - 样本 README：https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/README.MD
  - 样本目录 API：https://api.github.com/repos/Huibq/parakeet-crypto-rs/contents/sample?ref=main
- 可覆盖格式：
  - `.kgm`：`sample/test_kgm_v2.kgm`、`sample/test_kgm_v3.kgm`、`sample/test_kgm_v4.kgm`
  - `.qmcogg`：`sample/test_qmc1.qmcogg`
  - `.mgg`：`sample/test_qmc2_map.mgg`、`sample/test_qmc2_rc4.mgg`、`sample/test_qmc2_rc4_EncV2.mgg`
  - `.x2m`：`sample/test_xmly.x2m`
  - `.x3m`：`sample/test_xmly.x3m`
  - 附带密钥/表文件：`test_x2m_key.bin`、`test_x3m_key.bin`、`test_xmly_scramble_table.bin`、`test_kgm_v4_*_table.bin`。
- 许可/合规判断：
  - 仓库公开；GitHub API 标记许可证为 Apache-2.0；仓库根目录同时有 `LICENSE-Apache` 和 `LICENSE-MIT`。
  - 样本 README 明确说明：样本用于生成加密文件以便验证；原始 `test_121529_32kbps.ogg` 是用 ffmpeg 编码，音效来自 Pixabay 用户 `royalty_free_music`。
  - 该说明比普通个人上传歌曲样本更清晰，适合作为合规评测样本来源。
- 可下载性：
  - 可直接通过每个文件的 `download_url` 下载，例如：
    - https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v2.kgm
    - https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v3.kgm
    - https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v4.kgm
    - https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc1.qmcogg
    - https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc2_map.mgg
    - https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc2_rc4.mgg
    - https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc2_rc4_EncV2.mgg
    - https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_xmly.x2m
    - https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_xmly.x3m
- 对本项目评测的建议：
  - 优先下载这些文件作为端到端转换评测样本。
  - 对 `.kgm` 建议至少评测 v2/v3/v4 三个样本，因为同一扩展名存在不同头版本。
  - 对 `.mgg` 建议分别评测 map、rc4、EncV2 三个样本，因为 README/实现显示 QMCv2 存在多种加密模式。
  - `.x2m` / `.x3m` 可能依赖随样本提供的 key 文件；若 MusicDecrypto CLI 不能自动识别配套密钥，应记录为失败或需额外参数，不要硬编码绕过。

## 本地已有样本

- 来源 URL：无，仓库本地已有。
- 本地文件：
  - `./Lost Frequencies、Janieck - Reality.kgm`
  - `./徐梦圆 - China-X.kgm`
  - `./越人歌 (钢琴伴奏).kgm`
- 可覆盖格式：`.kgm`
- 许可/合规判断：
  - 未找到仓库内许可证或来源说明，不能作为「公开合规来源」证明。
  - 可用于开发者本地自检，但评测报告应标记为「本地已有，来源/授权未核实」，不要随报告传播。
- 可下载性：不可公开下载。
- 对本项目评测的建议：
  - 如果使用，只记录本地路径、文件大小和不可复分发限制。
  - 优先使用 `parakeet-crypto-rs` 的 `.kgm` 样本作为可复查基准。

## 未采纳来源/风险来源

- `ix64/unlock-music` GitHub 仓库访问结果显示 `Repository access blocked`，原因是 DMCA，页面指向 GitHub DMCA 记录：`https://github.com/github/dmca/blob/master/2022/11/2022-11-04-qqmusic.md`。
- `git.unlock-music.dev/um/web` 通过普通 HTTP 访问时遇到 Cloudflare challenge，未能在本次调研中取得可复查样本页面。
- 多个博客、论坛、网盘类结果以工具教程或用户歌曲为主，没有清晰许可，不采纳为测试样本来源。

## 按本项目声明格式的覆盖建议

| 格式 | 调研状态 | 推荐来源/说明 |
|---|---|---|
| `ncm` | 未找到合规公开完整样本 | 可记录「未覆盖：缺少合规样本」。MusicDecrypto/libtakiyasha 仅提供实现或文档，未发现可复查完整样本。 |
| `tm2` | 未找到合规公开样本 | 记录未覆盖。 |
| `tm6` | 未找到合规公开样本 | 记录未覆盖。 |
| `qmc0` | 仅找到算法片段 | MusicDecrypto 有 `qmc0-static.payload(.enc)`，不是完整容器；端到端评测建议标记未覆盖。 |
| `qmc2` | 未找到合规公开完整样本 | 记录未覆盖。 |
| `qmc3` | 未找到合规公开完整样本 | 记录未覆盖。 |
| `qmc4` | 未找到合规公开完整样本 | 记录未覆盖。 |
| `qmc6` | 未找到合规公开完整样本 | 记录未覆盖。 |
| `qmc8` | 未找到合规公开完整样本 | 记录未覆盖。 |
| `qmcogg` | 找到合规公开样本 | 使用 `parakeet-crypto-rs/sample/test_qmc1.qmcogg`。 |
| `qmcflac` | 未找到合规公开完整样本 | 记录未覆盖。 |
| `tkm` | 未找到合规公开样本 | 记录未覆盖。 |
| `bkcmp3` | 未找到合规公开样本 | 记录未覆盖。 |
| `bkcm4a` | 未找到合规公开样本 | 记录未覆盖。 |
| `bkcwma` | 未找到合规公开样本 | 记录未覆盖。 |
| `bkcogg` | 未找到合规公开样本 | 记录未覆盖。 |
| `bkcwav` | 未找到合规公开样本 | 记录未覆盖。 |
| `bkcape` | 未找到合规公开样本 | 记录未覆盖。 |
| `bkcflac` | 未找到合规公开样本 | 记录未覆盖。 |
| `mgg` | 找到合规公开样本 | 使用 `parakeet-crypto-rs/sample/test_qmc2_map.mgg`、`test_qmc2_rc4.mgg`、`test_qmc2_rc4_EncV2.mgg`。 |
| `mgg1` | 未找到对应扩展名样本 | 可尝试同族 `.mgg` 作为算法基线，但逐项报告中应标记 `mgg1` 未覆盖。 |
| `mggl` | 未找到对应扩展名样本 | 记录未覆盖。 |
| `mflac` | 仅找到算法片段 | MusicDecrypto 有测试数据片段，不是完整容器；端到端评测建议标记未覆盖。 |
| `mflac0` | 仅找到算法片段 | MusicDecrypto 有测试数据片段，不是完整容器；端到端评测建议标记未覆盖。 |
| `mmp4` | 未找到合规公开样本 | 记录未覆盖。 |
| `6d7033` | 未找到合规公开样本 | 这是 QMC 十六进制后缀，记录未覆盖。 |
| `6d3461` | 未找到合规公开样本 | 这是 QMC 十六进制后缀，记录未覆盖。 |
| `6f6767` | 未找到合规公开样本 | 这是 QMC 十六进制后缀，记录未覆盖。 |
| `776176` | 未找到合规公开样本 | 这是 QMC 十六进制后缀，记录未覆盖。 |
| `666c6163` | 未找到合规公开样本 | 这是 QMC 十六进制后缀，记录未覆盖。 |
| `kgm` | 找到合规公开样本 | 使用 `parakeet-crypto-rs/sample/test_kgm_v2.kgm`、`test_kgm_v3.kgm`、`test_kgm_v4.kgm`；本地已有 `.kgm` 仅作辅助。 |
| `kgma` | 未找到合规公开样本 | 记录未覆盖。 |
| `vpr` | 未找到完整容器样本 | parakeet 仓库有 VPR 测试向量但未发现 `sample/*.vpr` 完整样本。 |
| `kwm` | 未找到合规公开样本 | 记录未覆盖。 |
| `x2m` | 找到合规公开样本 | 使用 `parakeet-crypto-rs/sample/test_xmly.x2m`，注意配套 key。 |
| `x3m` | 找到合规公开样本 | 使用 `parakeet-crypto-rs/sample/test_xmly.x3m`，注意配套 key。 |
| `xm` | 未找到合规公开样本 | 记录未覆盖。 |
| `.qmc*` 前缀变种 | 部分覆盖 | `.qmcogg` 可覆盖 qmc 前缀识别的一种真实样本；未找到 `.qmc999` 这类公开样本。 |

## 建议下载清单

仅建议下载小体积、公开、可复查样本到临时/忽略目录，例如 `.trellis/tasks/06-11-format-evaluation/tmp-samples/` 或项目 `.gitignore` 覆盖的临时目录：

```text
https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v2.kgm
https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v3.kgm
https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_kgm_v4.kgm
https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc1.qmcogg
https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc2_map.mgg
https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc2_rc4.mgg
https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_qmc2_rc4_EncV2.mgg
https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_xmly.x2m
https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_xmly.x3m
https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_x2m_key.bin
https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_x3m_key.bin
https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/test_xmly_scramble_table.bin
```

## 复查命令线索

```bash
curl -L -s "https://api.github.com/repos/davidxuang/MusicDecrypto/contents/MusicDecrypto.Library.Tests/DataSets?ref=master"
curl -L -s "https://raw.githubusercontent.com/davidxuang/MusicDecrypto/master/MusicDecrypto.Library/DecryptoFactory.cs"
curl -L -s "https://api.github.com/repos/Huibq/parakeet-crypto-rs/contents/sample?ref=main"
curl -L -s "https://raw.githubusercontent.com/Huibq/parakeet-crypto-rs/main/sample/README.MD"
```
