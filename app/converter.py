import json
import subprocess
from pathlib import Path

from app.config import SUPPORTED_OUTPUT_FORMATS
from app.decryptor import DecryptError, cleanup_decrypted_path, decrypt_audio_to_temp, is_encrypted_audio_file
from app.ffmpeg_tools import get_ffmpeg_path, get_ffprobe_path
from app.file_ops import build_output_path, is_supported_input, make_unique_path
from app.models import ConvertResult, SourceItem


class ConvertError(Exception):
    """Raised when audio conversion validation fails."""
    pass


def build_failed_result(source_path: Path, message: str) -> ConvertResult:
    return ConvertResult(source_path, None, False, message)


def probe_audio(path: Path) -> None:
    """
    Verify that the file contains valid audio streams using ffprobe.

    Raises ConvertError if the file is invalid or has no audio streams.
    """
    ffprobe = get_ffprobe_path()
    command = [
        str(ffprobe),
        "-v",
        "error",
        "-show_entries",
        "stream=codec_type",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        message = result.stderr.strip() or "无法读取音频信息"
        raise ConvertError(message)
    data = json.loads(result.stdout or "{}")
    streams = data.get("streams", [])
    if not any(item.get("codec_type") == "audio" for item in streams):
        raise ConvertError("文件中未检测到音频流")


def build_ffmpeg_command(source_path: Path, output_path: Path) -> list[str]:
    ffmpeg = get_ffmpeg_path()
    return [
        str(ffmpeg),
        "-y",
        "-i",
        str(source_path),
        str(output_path),
    ]


def convert_one(source_path: Path, output_path: Path, target_format: str) -> ConvertResult:
    """
    Convert a single audio file to the target format.

    Handles both plain and encrypted audio files. For encrypted files,
    decrypts to a temporary location first, then converts the decrypted file.
    """
    if target_format not in SUPPORTED_OUTPUT_FORMATS:
        return build_failed_result(source_path, "不支持的输出格式")
    if not source_path.is_file():
        return build_failed_result(source_path, "源文件不存在")
    if not is_supported_input(source_path):
        return build_failed_result(source_path, "不支持的输入格式")

    actual_source_path = source_path
    cleanup_path: Path | None = None
    try:
        if is_encrypted_audio_file(source_path):
            actual_source_path = decrypt_audio_to_temp(source_path)
            cleanup_path = actual_source_path
        probe_audio(actual_source_path)
        command = build_ffmpeg_command(actual_source_path, output_path)
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            message_lines = result.stderr.strip().splitlines()
            message = message_lines[-1] if message_lines else "转换失败"
            return build_failed_result(source_path, message)
        return ConvertResult(source_path, output_path, True, "转换成功")
    except FileNotFoundError:
        return build_failed_result(source_path, "未找到 ffmpeg、ffprobe 或解密工具，请检查内置文件")
    except DecryptError:
        return build_failed_result(source_path, "解密失败，请检查文件是否受支持")
    except ConvertError as error:
        return build_failed_result(source_path, str(error))
    except json.JSONDecodeError:
        return build_failed_result(source_path, "音频探测结果解析失败")
    finally:
        cleanup_decrypted_path(cleanup_path)


def convert_many(items: list[SourceItem], output_dir: Path, target_format: str) -> list[ConvertResult]:
    """Convert multiple audio files, ensuring unique output paths for conflicts."""
    results: list[ConvertResult] = []
    for item in items:
        output_path = build_output_path(output_dir, item.relative_path, target_format)
        output_path = make_unique_path(output_path)
        result = convert_one(item.source_path, output_path, target_format)
        results.append(result)
    return results
