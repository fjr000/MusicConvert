from app.decryptor import DecryptError, decrypt_audio_to_temp, is_encrypted_audio_file

KgmError = DecryptError


def is_kgm_file(path):
    return is_encrypted_audio_file(path) and path.suffix.lower() in {".kgm", ".kgma", ".vpr"}


def decrypt_kgm_to_temp(source_path):
    return decrypt_audio_to_temp(source_path)
