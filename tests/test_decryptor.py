import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.decryptor import build_decrypt_command, cleanup_decrypted_path, decrypt_audio_to_temp, is_encrypted_audio_file


class DecryptorTestCase(unittest.TestCase):
    def test_is_encrypted_audio_file_accepts_known_suffix(self) -> None:
        self.assertTrue(is_encrypted_audio_file(Path("a.ncm")))
        self.assertTrue(is_encrypted_audio_file(Path("a.kwm")))

    def test_is_encrypted_audio_file_accepts_qmc_prefix(self) -> None:
        self.assertTrue(is_encrypted_audio_file(Path("a.qmc999")))

    def test_is_encrypted_audio_file_rejects_plain_audio(self) -> None:
        self.assertFalse(is_encrypted_audio_file(Path("a.mp3")))

    def test_build_decrypt_command_uses_extensive_for_qmc_prefix(self) -> None:
        command = build_decrypt_command(Path("a.qmc999"))

        self.assertIn("-x", command)
        self.assertEqual(command[-1], "a.qmc999")

    def test_build_decrypt_command_skips_extensive_for_known_suffix(self) -> None:
        command = build_decrypt_command(Path("a.ncm"))

        self.assertNotIn("-x", command)
        self.assertEqual(command[-1], "a.ncm")

    @patch("app.decryptor.subprocess.run")
    def test_decrypt_audio_to_temp_reads_output_from_staged_directory(self, run_mock) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "a.qmc0"
            source.write_bytes(b"encrypted")

            def fake_run(command, capture_output, text):
                staged_source = Path(command[-1])
                staged_source.with_name("a.mp3").write_bytes(b"ID3")
                return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()

            run_mock.side_effect = fake_run
            output = decrypt_audio_to_temp(source)
            staged_source = output.with_suffix(".qmc0")

            self.assertTrue(output.exists())
            self.assertEqual(output.name, "a.mp3")
            self.assertEqual(output.read_bytes(), b"ID3")
            self.assertTrue(staged_source.exists())
            cleanup_decrypted_path(output)
            self.assertFalse(output.parent.exists())


if __name__ == "__main__":
    unittest.main()
