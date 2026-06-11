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

---

## Scenario: Windows GUI external CLI subprocesses

### 1. Scope / Trigger
- Trigger: adding or changing `subprocess.run` calls for bundled external CLI tools used from the desktop GUI.
- Applies to `ffprobe`, `ffmpeg`, `MusicDecrypto`, and future tool executables launched during conversion.

### 2. Signatures
- Use `hidden_subprocess_kwargs()` from `app.subprocess_utils` and pass it into `subprocess.run`:
```python
result = subprocess.run(command, capture_output=True, text=True, **hidden_subprocess_kwargs())
```

### 3. Contracts
- On Windows (`os.name == "nt"`) with `subprocess.CREATE_NO_WINDOW` available, pass `creationflags=subprocess.CREATE_NO_WINDOW`.
- On non-Windows platforms, return `{}` and do not pass Windows-only `creationflags`.
- Do not change stdout/stderr capture, text decoding, return-code handling, or error parsing when adding this helper.

### 4. Validation & Error Matrix
- Windows GUI subprocess without hidden flags -> visible CMD console popup for each conversion.
- Non-Windows subprocess with Windows-only `creationflags` -> platform-specific failure risk.
- Missing CLI executable -> preserve existing `FileNotFoundError` handling and user-facing missing-tool message.

### 5. Good/Base/Bad Cases
- Good: every external conversion/decryption CLI call uses `**hidden_subprocess_kwargs()` and existing parsing stays unchanged.
- Base: direct CLI call in tests can mock `hidden_subprocess_kwargs()` to assert the propagated kwargs.
- Bad: hardcoding `creationflags` at each call site or passing it unconditionally on non-Windows.

### 6. Tests Required
- Unit test `hidden_subprocess_kwargs()` for Windows and non-Windows branches.
- Unit test each conversion/decryption subprocess call that must propagate the hidden-window kwargs.
- Run `.venv/Scripts/python.exe -m unittest discover -s tests`.
- Run `.venv/Scripts/python.exe -m compileall -q app tests`.

### 7. Wrong vs Correct
#### Wrong
```python
result = subprocess.run(command, capture_output=True, text=True)
```

#### Correct
```python
result = subprocess.run(command, capture_output=True, text=True, **hidden_subprocess_kwargs())
```
