# Quality Guidelines

> Code quality standards for backend development.

---

## Overview

<!--
Document your project's quality standards here.

Questions to answer:
- What patterns are forbidden?
- What linting rules do you enforce?
- What are your testing requirements?
- What code review standards apply?
-->

(To be filled by the team)

---

## Forbidden Patterns

<!-- Patterns that should never be used and why -->

(To be filled by the team)

---

## Required Patterns

<!-- Patterns that must always be used -->

(To be filled by the team)

---

## Testing Requirements

<!-- What level of testing is expected -->

(To be filled by the team)

---

## Code Review Checklist

<!-- What reviewers should check -->

(To be filled by the team)

---

## Scenario: PyInstaller one-folder bundled tools

### 1. Scope / Trigger
- Trigger: packaging the Windows desktop app with `music_converter.spec` or adding external CLI tools under `tools/`.
- Keep application code and PyInstaller config unchanged unless packaging is blocked by a verified runtime failure.

### 2. Signatures
- Build command: `.venv/Scripts/python.exe -m PyInstaller -y music_converter.spec`.
- Runtime lookup helpers: `get_ffmpeg_path()`, `get_ffprobe_path()`, `get_musicdecrypto_path()` return `Path` values for executable tools.

### 3. Contracts
- Source tool layout: `tools/<tool-dir>/<name>.exe`.
- PyInstaller 6 one-folder data layout: `dist/音乐格式转换器/_internal/tools/<tool-dir>/<name>.exe`.
- Runtime root in a frozen app is `Path(sys._MEIPASS)`, not the directory beside the top-level exe.

### 4. Validation & Error Matrix
- Missing source `tools/ffmpeg/ffmpeg.exe` or `ffprobe.exe` -> build may succeed, but conversion fails at runtime with missing-tool handling.
- Missing bundled `_internal/tools/ffmpeg/*.exe` after build -> package is incomplete.
- GUI command references a missing method -> exe exists but app startup is invalid; fix the direct method binding issue before release.

### 5. Good/Base/Bad Cases
- Good: source FFmpeg/FFprobe exist, PyInstaller succeeds, bundled files exist under `_internal/tools/ffmpeg/`, tests pass.
- Base: build output exe exists, but verify bundled data before declaring success.
- Bad: checking only `dist/音乐格式转换器/tools/ffmpeg/`; PyInstaller 6 puts data under `_internal`.

### 6. Tests Required
- Run `.venv/Scripts/python.exe -m unittest discover -s tests`.
- Run `.venv/Scripts/python.exe -m compileall -q app tests`.
- Verify `dist/音乐格式转换器/音乐格式转换器.exe` exists.
- Verify `dist/音乐格式转换器/_internal/tools/ffmpeg/ffmpeg.exe` and `ffprobe.exe` exist and `-version` exits successfully.

### 7. Wrong vs Correct
#### Wrong
```python
# Assuming bundled tools are beside the top-level exe in PyInstaller 6 one-folder mode.
Path("dist/音乐格式转换器/tools/ffmpeg/ffmpeg.exe")
```

#### Correct
```python
# Data files are available under sys._MEIPASS at runtime.
Path(sys._MEIPASS) / "tools" / "ffmpeg" / "ffmpeg.exe"
```
