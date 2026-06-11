# 整理项目文件准备远程仓库

## Goal

整理当前音乐格式转换器项目的仓库文件与目录结构，使其适合提交到远程仓库：保留必要源码、测试、文档和可复现构建信息，避免把本地缓存、构建产物、大型样本或不适合公开的二进制误提交。

## What I already know

* 用户希望“项目文件、文件结构整理，准备提交远程仓库”。
* 当前仓库是 Python 项目，主要代码在 `app/`，测试在 `tests/`，文档在 `docs/`，打包配置为 `music_converter.spec`。
* `.gitignore` 已排除 `__pycache__/`、`.pytest_cache/`、`dist/`、`build/`、`.venv/`、`tools/ffmpeg/*.exe`。
* `git status --short --untracked-files=all` 当前只显示本任务目录未跟踪；根目录的 `.kgm` 样本由 `.git/info/exclude` 本地排除，不会被当前机器提交，但不会随仓库共享。
* `tools/musicdecrypto/musicdecrypto.exe` 目前已被 Git 跟踪；`tools/ffmpeg/` 只跟踪 `THIRD_PARTY.md`，不跟踪 exe。
* 根目录可见本地/产物目录：`.venv/`、`.pytest_cache/`、`build/`、`dist/`，以及根目录 `.kgm` 样本文件和 `toolsmusicdecrypto` 文件/目录名异常项。

## Assumptions (temporary)

* “整理”优先指仓库提交边界和目录清理，不涉及应用功能改造。
* 不直接删除用户本地大文件；优先通过 `.gitignore`、文档和必要时移动到明确目录来避免误提交。
* 远程仓库可能是公开或半公开，因此第三方二进制、音频样本和本地构建产物需要谨慎处理。
* 用户已确认：`tools/musicdecrypto/musicdecrypto.exe` 不提交到远程仓库，但需要提供下载脚本或上游仓库/下载说明。

## Open Questions

* 无。

## Requirements (evolving)

* 检查并整理仓库顶层结构，让源码、测试、文档、工具说明的位置清晰。
* 更新忽略规则，避免提交本地虚拟环境、缓存、构建产物、音频样本和不应进仓库的二进制。
* 保留必要的第三方工具来源/许可证说明。
* 从 Git 跟踪中移除 `tools/musicdecrypto/musicdecrypto.exe`，改为通过共享忽略规则防止误提交。
* 提供开发者获取第三方工具的方式：README 链接说明，并新增 Windows 下载脚本。
* 下载脚本应同时准备 `ffmpeg.exe`、`ffprobe.exe` 和 `musicdecrypto.exe`，下载到既有工具目录：`tools/ffmpeg/` 与 `tools/musicdecrypto/`。
* 不破坏现有运行、测试、打包流程。

## Acceptance Criteria (evolving)

* [ ] `git status --short --untracked-files=all` 不再暴露无意提交的本地产物/样本。
* [ ] `.gitignore` 覆盖仓库共享层面的本地缓存、构建输出、音频样本、敏感/大型二进制规则。
* [ ] `tools/musicdecrypto/musicdecrypto.exe` 不再作为仓库跟踪文件提交。
* [ ] README 能说明开发者如何放置所需工具，并提供上游来源/下载方式。
* [ ] 新增下载脚本，能同时准备 `ffmpeg.exe`、`ffprobe.exe` 和 `musicdecrypto.exe`，下载目标清晰，不覆盖无关文件。
* [ ] `python -m unittest discover -s tests` 通过。
* [ ] `python -m compileall app tests` 通过。

## Technical Approach

* 采用“源码与说明入库、第三方 exe 本地准备”的结构：保留 `tools/*/THIRD_PARTY.md`，移除 `tools/musicdecrypto/musicdecrypto.exe` 的 Git 跟踪。
* 在 `.gitignore` 共享层面忽略工具 exe、常见音频样本、缓存和构建产物，避免依赖个人 `.git/info/exclude`。
* 新增 Windows PowerShell 脚本用于下载并解压/放置第三方工具；脚本只写入 `tools/ffmpeg/` 和 `tools/musicdecrypto/` 下的目标 exe。
* README 更新为：说明工具放置路径、下载脚本用法、上游来源与许可证提示。

## Decision (ADR-lite)

**Context**: 远程仓库需要可复现，但不应直接提交第三方二进制和本地样本。

**Decision**: 不提交 `musicdecrypto.exe` 等第三方 exe；通过 README 与下载脚本让开发者本地准备 `ffmpeg` / `ffprobe` / `musicdecrypto`。

**Consequences**: 仓库更干净，降低二进制分发和许可证风险；首次开发运行前需要执行脚本或手动放置工具。

## Definition of Done

* 测试通过。
* 编译检查通过。
* 远程提交前的文件清单清晰，未混入本地缓存、构建产物或样本音频。
* README / 相关说明与最终文件结构一致。

## Out of Scope

* 不修改音频转换、解密、GUI 等业务行为。
* 不新增远程仓库、不执行 `git push`。
* 不替用户决定第三方二进制的公开分发策略。

## Technical Notes

* 已检查：`README.md`、`.gitignore`、`git ls-files`、`git status --short --untracked-files=all`、`git check-ignore`。
* 当前 `.gitignore` 未共享忽略 `*.kgm`，样本音频仅依赖本机 `.git/info/exclude`。
* 当前 `tools/musicdecrypto/musicdecrypto.exe` 是已跟踪文件，需要显式 `git rm --cached` 并更新说明。
* `tools/musicdecrypto/THIRD_PARTY.md` 已记录上游仓库 `https://github.com/davidxuang/MusicDecrypto` 和版本 `v2.4.2`。
* `tools/ffmpeg/THIRD_PARTY.md` 已记录 BtbN FFmpeg Windows LGPL 构建下载地址。
