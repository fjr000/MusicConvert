import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from app.config import ENCRYPTED_AUDIO_PREFIXES, ENCRYPTED_AUDIO_SUFFIXES
from app.ffmpeg_tools import get_musicdecrypto_path


class DecryptError(Exception):
    pass


def is_encrypted_audio_file(path: Path) -> bool:
    suffix = path.suffix.lower()
    if suffix in ENCRYPTED_AUDIO_SUFFIXES:
        return True
    return any(suffix.startswith(prefix) for prefix in ENCRYPTED_AUDIO_PREFIXES)


def build_decrypt_command(source_path: Path) -> list[str]:
    command = [
        str(get_musicdecrypto_path()),
        "-f",
    ]
    if _needs_extensive_detection(source_path):
        command.append("-x")
    command.append(str(source_path))
    return command


def _needs_extensive_detection(source_path: Path) -> bool:
    return any(source_path.suffix.lower().startswith(prefix) for prefix in ENCRYPTED_AUDIO_PREFIXES)


def decrypt_audio_to_temp(source_path: Path) -> Path:
    temp_dir = Path(tempfile.mkdtemp(prefix="music-convert-decrypt-"))
    staged_source = temp_dir / source_path.name
    shutil.copy2(source_path, staged_source)
    command = build_decrypt_command(staged_source)
    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except FileNotFoundError:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise

    output_files = [item for item in temp_dir.iterdir() if item.is_file() and item != staged_source]
    if result.returncode != 0 or len(output_files) != 1:
        cleanup_decrypted_path(staged_source)
        raise DecryptError("文件解密失败")
    return output_files[0]


def cleanup_decrypted_path(path: Path | None) -> None:
    if path is None:
        return
    parent = path.parent
    for _ in range(5):
        blocked = False
        for item in parent.iterdir():
            if not item.is_file():
                continue
            try:
                item.unlink(missing_ok=True)
            except PermissionError:
                blocked = True
        if not blocked:
            break
        time.sleep(0.2)
    shutil.rmtree(parent, ignore_errors=True)
