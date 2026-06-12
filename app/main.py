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


def _ensure_ffmpeg() -> None:
    """精简版首次启动时下载 FFmpeg（完整版已随包，跳过检查）"""
    if not getattr(sys, "frozen", False):
        return  # 开发模式不检查

    from app.ffmpeg_tools import get_runtime_root
    from app.ffmpeg_downloader import ensure_ffmpeg

    tools_dir = get_runtime_root() / "tools"
    if not ensure_ffmpeg(tools_dir):
        sys.exit(1)


if __name__ == "__main__":
    _chdir_to_app_dir()
    _ensure_ffmpeg()
    run_app()
