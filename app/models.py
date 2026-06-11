from dataclasses import dataclass
from pathlib import Path


@dataclass
class SourceItem:
    source_path: Path
    relative_path: Path


@dataclass
class ConvertResult:
    source_path: Path
    output_path: Path | None
    success: bool
    message: str
