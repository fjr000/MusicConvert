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

## Common Mistakes

- Mixing validation failures with crash-level failures.
- Returning technical errors directly to users without a readable Chinese message.
- Forgetting that batch mode and single-file mode share the same conversion contract.
