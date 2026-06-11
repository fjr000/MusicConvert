# brainstorm: support more encrypted audio formats

## Goal

在现有 `.kgm` 支持基础上，为这个本地离线音乐转换工具新增“其他加密音频格式”的输入支持，并尽量复用现有的探测与转码流程，保持最小改动和可读报错。

## What I already know

- 当前项目是 Windows 本地桌面工具，核心转换链路依赖内置 `ffprobe` / `ffmpeg`。
- 当前支持的普通输入格式见 `app/config.py`，加密格式只有 `.kgm`。
- 当前 `.kgm` 的接入方式是：识别扩展名后先本地解密到临时文件，再调用现有 `probe_audio()` 与 `ffmpeg` 转换。
- 当前单文件失败不会中断整批转换。
- README 已明确：不承诺支持冷门、私有或 DRM 音频格式。

## Assumptions (temporary)

- 新增格式也应优先复用 `.kgm` 这套“前置解密/解包，再进入现有流程”的模式。
- 首版仍以本地离线可处理为前提，不依赖联网取密钥。
- 允许引入成熟的本地离线开源依赖处理 `ncm` / `qmc*`。
- 已选定优先使用 `MusicDecrypto` 作为统一离线解密方案。
- 如果同一依赖同时支持 `kgm` / `ncm` / `qmc*`，首版可一并替换现有 `kgm` 实现。
- `MusicDecrypto` 按随程序分发的外部 CLI 二进制方式接入。
- 首版只分发并支持 `MusicDecrypto` 的 Windows `x64` CLI。
- 不会一次性承诺支持所有历史变种。

## Open Questions

- 暂无

## Requirements (evolving)

- 首版支持 `MusicDecrypto` 支持的可明确识别加密输入格式。
- `qmc*` 按通配前缀范围识别，而不是只列少数固定后缀。
- 腾讯系格式识别按 `MusicDecrypto` 已支持的 QQ 音乐常见变种整组收口，而不只限字面 `qmc` 前缀。
- 与普通音频同名的重叠后缀（如普通 `.mp3` / `.flac` 这类）首版不纳入额外加密探测分支，避免影响现有普通音频流程。
- 接受“能识别但个别变种仍可能解密失败”，并用简短中文提示兜底。
- 第三方依赖失败时，用户侧统一使用短中文文案，不直接暴露底层长日志或堆栈。
- 能成功解密时继续复用现有转换流程。
- 解密失败时仅当前文件失败，并返回简短中文提示。
- 保持现有普通音频格式行为不变。

## Acceptance Criteria (evolving)

- [ ] `MusicDecrypto` 首版支持的明确加密扩展名可被识别为输入格式。
- [ ] 首版支持格式可在本地离线场景下完成前置解密或解包。
- [ ] 解密产物可被现有 `ffprobe` / `ffmpeg` 流程正常处理。
- [ ] 某个加密文件失败时，不影响同批其他文件。
- [ ] 至少覆盖成功路径和失败路径测试。
- [ ] 自动化测试覆盖核心流程，另补真实样本手工验证。

## Definition of Done (team quality bar)

- Tests added/updated (unit/integration where appropriate)
- Lint / typecheck / CI green
- Docs/notes updated if behavior changes
- Rollout/rollback considered if risky

## Out of Scope (explicit)

- 与普通音频输入后缀重名、需要额外插入加密探测分支的格式首版不支持。
- 一次性支持所有市面上的加密音频格式。
- 需要联网、登录、动态拉取密钥的方案。
- 为冷门、私有或强 DRM 格式做兼容承诺。

## Technical Notes

- 当前加密接入点：`app/converter.py`
- 当前 KGM 实现：`app/kgm.py`
- 当前输入格式声明：`app/config.py`
- 当前用户文档：`README.md`
