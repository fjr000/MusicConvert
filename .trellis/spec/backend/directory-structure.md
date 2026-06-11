# Directory Structure

> How backend code is organized in this project.

---

## Overview

This project currently uses a small Python desktop-app layout instead of a web backend. Backend-like responsibilities here mean conversion orchestration, ffmpeg probing, path planning, and result models.

---

## Directory Layout

```text
app/
├── config.py
├── converter.py
├── ffmpeg_tools.py
├── file_ops.py
└── models.py
```

---

## Module Organization

- `config.py` stores supported format constants.
- `models.py` stores small dataclasses shared across modules.
- `file_ops.py` handles input collection, relative path mapping, and unique output naming.
- `ffmpeg_tools.py` resolves bundled runtime tool paths.
- `converter.py` owns probing, ffmpeg command building, and sequential conversion flow.

Keep modules flat until there is real pressure to split them.

---

## Naming Conventions

- Use simple searchable file names.
- Keep one responsibility per module.
- Prefer verb-style function names for operations like `collect_*`, `build_*`, `convert_*`, `get_*`.

---

## Examples

- `app/file_ops.py`
- `app/converter.py`
