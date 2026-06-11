import os
import sys
from pathlib import Path

from app.gui import run_app


def _chdir_to_app_dir() -> None:
    """In a frozen build, anchor the working directory to the exe folder.

    This keeps relative paths like the default "outputs" stable no matter
    where the portable exe is launched from (double-click, shortcut, CLI).
    """
    if getattr(sys, "frozen", False):
        os.chdir(Path(sys.executable).resolve().parent)


if __name__ == "__main__":
    _chdir_to_app_dir()
    run_app()
