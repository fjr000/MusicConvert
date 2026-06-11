# Directory Structure

> How frontend code is organized in this project.

---

## Overview

This project uses `tkinter` as a minimal desktop GUI. Frontend structure is intentionally small: one GUI module owns widgets and event wiring, while conversion logic stays outside the GUI layer.

---

## Directory Layout

```text
app/
├── gui.py
└── main.py
```

---

## Module Organization

- `main.py` is only the app entry point.
- `gui.py` owns window creation, widget layout, user actions, and result display.
- GUI code calls service-style functions from backend-like modules and should not reimplement conversion logic.

---

## Naming Conventions

- Keep widget-building helpers private with `_build_*` style names.
- Keep user actions as clear verb names like `pick_files`, `pick_folder`, `pick_output_dir`, `start_convert`.
- Keep GUI state in a small number of instance fields.

---

## Examples

- `app/main.py`
- `app/gui.py`
