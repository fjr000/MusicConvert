# Error Handling

> How errors are handled in this project.

---

## Overview

This project is a local desktop tool, so errors are not returned through an HTTP API. Errors should be converted into user-readable result messages and batch processing must continue when a single file fails.

---

## Error Types

### `ConvertError`

Use `ConvertError` for expected probe/validation failures discovered during conversion preparation.

---

## Error Handling Patterns

### Scenario: Batch audio conversion

#### 1. Scope / Trigger
- Trigger: local GUI action starts conversion across one or many files.

#### 2. Signatures
- `convert_one(source_path: Path, output_path: Path, target_format: str) -> ConvertResult`
- `convert_many(items: list[SourceItem], output_dir: Path, target_format: str) -> list[ConvertResult]`

#### 3. Contracts
- Input file missing -> return failed `ConvertResult`
- Unsupported input suffix -> return failed `ConvertResult`
- Unsupported output format -> return failed `ConvertResult`
- `ffprobe` parse/probe failure -> return failed `ConvertResult`
- `ffmpeg` execution failure -> return failed `ConvertResult`
- Batch flow must not raise for one-file failure when remaining items can still run

#### 4. Validation & Error Matrix
- bad output format -> `不支持的输出格式`
- missing source file -> `源文件不存在`
- unsupported input -> `不支持的输入格式`
- no audio stream -> `文件中未检测到音频流`
- ffmpeg/ffprobe missing -> `未找到 ffmpeg 或 ffprobe，请检查内置文件`
- ffprobe stderr present -> use readable stderr tail when possible

#### 5. Good/Base/Bad Cases
- Good: valid audio file converts and returns `success=True`
- Base: one file fails in batch and later files still execute
- Bad: first failing file raises and terminates the whole batch loop

#### 6. Tests Required
- Unit test unsupported output format
- Unit test successful conversion with mocked subprocess
- Unit test batch relative output behavior
- Unit test unsupported files are skipped before conversion

#### 7. Wrong vs Correct
##### Wrong
- Raise raw subprocess exceptions into the GUI loop for normal file-level failures
- Stop the whole batch on the first bad file

##### Correct
- Convert file-level failures into `ConvertResult.message`
- Keep iterating in `convert_many()` and summarize failures at the end

---

### Scenario: Encrypted input preprocessing

#### 1. Scope / Trigger
- Trigger: supported input is an encrypted container such as `.kgm`, `.ncm`, or QQ music encrypted variants, which must be decrypted to a temporary plain-audio file before probe and ffmpeg steps can run.

#### 2. Signatures
- `is_encrypted_audio_file(path: Path) -> bool`
- `decrypt_audio_to_temp(source_path: Path) -> Path`
- `cleanup_decrypted_path(path: Path | None) -> None`
- `convert_one(source_path: Path, output_path: Path, target_format: str) -> ConvertResult`

#### 3. Contracts
- Encrypted-input preprocessing happens inside `convert_one()` and remains transparent to GUI and batch callers.
- Decrypt success -> use the temporary plain-audio file for `ffprobe` and `ffmpeg`.
- Decrypt success must require the decrypt tool to create exactly one output file; do not rely only on the decrypt process exit code.
- Decrypt failure -> return failed `ConvertResult` with a short Chinese message such as `解密失败，请检查文件是否受支持`.
- Temporary decrypted files are intermediate artifacts only and must be deleted in `finally`, regardless of later probe/convert success.
- Do not expose raw stack traces or full tool logs to the user-facing result list.
- Plain audio formats with overlapping suffixes such as normal `.mp3` / `.flac` must not enter the encrypted-input branch unless the product explicitly adds an extra detection step.

#### 4. Validation & Error Matrix
- unsupported encrypted variant or tool failure -> `解密失败，请检查文件是否受支持`
- decrypt succeeded but probe failed -> return normal probe failure message and still delete temp file
- decrypt succeeded but ffmpeg failed -> return readable ffmpeg tail message and still delete temp file
- decrypt tool missing -> `未找到 ffmpeg、ffprobe 或解密工具，请检查内置文件`

#### 5. Good/Base/Bad Cases
- Good: encrypted input decrypts to temp audio, converts successfully, temp file is deleted
- Base: one encrypted file decrypt fails and only that file returns a readable failure
- Bad: decrypted temp file or temp directory is left on disk after success or failure

#### 6. Tests Required
- Unit test encrypted success path uses decrypted temp file as ffmpeg input and deletes it afterward
- Unit test decrypt failure returns the short readable message
- Unit test probe failure after decrypt still deletes the temp file
- Unit test encrypted suffix recognition covers both explicit suffixes and supported prefix-based variants

#### 7. Wrong vs Correct
##### Wrong
- Add encrypted formats as normal suffixes and send them directly to `ffprobe`
- Route plain `.mp3` / `.flac` inputs through encrypted detection without an explicit product decision
- Leave decrypted temp files in the output directory or temp directory
- Return raw decrypt implementation details to end users

##### Correct
- Treat encrypted formats as a preprocessing stage before the shared audio pipeline
- Always clean temporary decrypted artifacts in `finally`
- Keep user-facing failure text short and readable
- Keep plain audio flow unchanged unless a separate encrypted detection branch is intentionally introduced

## Common Mistakes

- Mixing validation failures with crash-level failures.
- Returning technical errors directly to users without a readable Chinese message.
- Forgetting that batch mode and single-file mode share the same conversion contract.
- Adding encrypted formats as plain suffix support without a preprocessing step.
- Treating an encrypted suffix as fully covered without testing real complete samples for the specific format variant.
