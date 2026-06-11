SUPPORTED_INPUT_FORMATS = (
    "mp3",
    "wav",
    "flac",
    "m4a",
    "aac",
    "ogg",
    "opus",
    "wma",
    "kgm",
)

SUPPORTED_OUTPUT_FORMATS = (
    "mp3",
    "wav",
    "flac",
    "m4a",
    "aac",
    "ogg",
    "opus",
)

AUDIO_SUFFIXES = tuple(f".{item}" for item in SUPPORTED_INPUT_FORMATS)
