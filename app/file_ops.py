from pathlib import Path

from app.config import AUDIO_SUFFIXES
from app.models import SourceItem


def is_supported_input(path: Path) -> bool:
    return path.suffix.lower() in AUDIO_SUFFIXES


def collect_file_items(paths: list[str]) -> list[SourceItem]:
    items: list[SourceItem] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_file() and is_supported_input(path):
            items.append(SourceItem(source_path=path, relative_path=Path(path.name)))
    return items


def collect_folder_items(folder: str) -> list[SourceItem]:
    root = Path(folder)
    items: list[SourceItem] = []
    for path in root.rglob("*"):
        if path.is_file() and is_supported_input(path):
            items.append(SourceItem(source_path=path, relative_path=path.relative_to(root)))
    return items


def build_output_path(output_dir: Path, relative_path: Path, target_format: str) -> Path:
    target_relative = relative_path.with_suffix(f".{target_format}")
    output_path = output_dir / target_relative
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def make_unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    index = 1
    while True:
        candidate = path.with_name(f"{path.stem}_{index}{path.suffix}")
        if not candidate.exists():
            return candidate
        index += 1
