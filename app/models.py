from dataclasses import dataclass
from pathlib import Path


@dataclass
class SourceItem:
    """Represents an input audio file with its relative path for output structure."""
    source_path: Path
    relative_path: Path


@dataclass
class ConvertResult:
    """Result of a single file conversion operation."""
    source_path: Path
    output_path: Path | None
    success: bool
    message: str
