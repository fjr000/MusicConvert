SUPPORTED_AUDIO_INPUT_FORMATS = (
    "mp3",
    "wav",
    "flac",
    "m4a",
    "aac",
    "ogg",
    "opus",
    "wma",
)

SUPPORTED_ENCRYPTED_INPUT_FORMATS = (
    "ncm",
    "tm2",
    "tm6",
    "qmc0",
    "qmc2",
    "qmc3",
    "qmc4",
    "qmc6",
    "qmc8",
    "qmcogg",
    "qmcflac",
    "tkm",
    "bkcmp3",
    "bkcm4a",
    "bkcwma",
    "bkcogg",
    "bkcwav",
    "bkcape",
    "bkcflac",
    "mgg",
    "mgg1",
    "mggl",
    "mflac",
    "mflac0",
    "mmp4",
    "6d7033",
    "6d3461",
    "6f6767",
    "776176",
    "666c6163",
    "kgm",
    "kgma",
    "vpr",
    "kwm",
    "x2m",
    "x3m",
    "xm",
)

ENCRYPTED_AUDIO_PREFIXES = (
    ".qmc",
)

SUPPORTED_INPUT_FORMATS = SUPPORTED_AUDIO_INPUT_FORMATS + SUPPORTED_ENCRYPTED_INPUT_FORMATS

SUPPORTED_OUTPUT_FORMATS = (
    "mp3",
    "wav",
    "flac",
    "m4a",
    "aac",
    "ogg",
    "opus",
)

AUDIO_SUFFIXES = tuple(f".{item}" for item in SUPPORTED_AUDIO_INPUT_FORMATS)
ENCRYPTED_AUDIO_SUFFIXES = tuple(f".{item}" for item in SUPPORTED_ENCRYPTED_INPUT_FORMATS)
