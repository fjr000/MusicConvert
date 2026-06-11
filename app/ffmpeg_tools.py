import sys
from pathlib import Path


def get_runtime_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def get_tool_path(tool_dir: str, name: str) -> Path:
    file_name = f"{name}.exe"
    root = get_runtime_root()
    bundled = root / "tools" / tool_dir / file_name
    if bundled.exists():
        return bundled
    local = Path.cwd() / "tools" / tool_dir / file_name
    if local.exists():
        return local
    return Path(file_name)


def get_ffmpeg_path() -> Path:
    return get_tool_path("ffmpeg", "ffmpeg")


def get_ffprobe_path() -> Path:
    return get_tool_path("ffmpeg", "ffprobe")


def get_musicdecrypto_path() -> Path:
    return get_tool_path("musicdecrypto", "musicdecrypto")
