# DEPRECATED: This module is a redundant wrapper.
# Use app.decryptor functions directly instead.
from app.decryptor import DecryptError as KgmError
from app.decryptor import decrypt_audio_to_temp as decrypt_kgm_to_temp
from app.decryptor import is_encrypted_audio_file


def is_kgm_file(path):
    """DEPRECATED: Use is_encrypted_audio_file() instead."""
    return is_encrypted_audio_file(path) and path.suffix.lower() in {".kgm", ".kgma", ".vpr"}
