import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.converter import convert_many, convert_one
from app.decryptor import DecryptError
from app.models import SourceItem


class ConverterTestCase(unittest.TestCase):
    def test_convert_one_rejects_bad_output_format(self) -> None:
        result = convert_one(Path("a.mp3"), Path("b.xxx"), "xxx")
        self.assertFalse(result.success)
        self.assertEqual(result.message, "不支持的输出格式")

    @patch("app.converter.subprocess.run")
    def test_convert_one_success(self, run_mock) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "a.mp3"
            output = root / "b.wav"
            source.write_bytes(b"1")

            run_mock.side_effect = [
                type("Result", (), {"returncode": 0, "stdout": '{"streams":[{"codec_type":"audio"}]}', "stderr": ""})(),
                type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})(),
            ]

            result = convert_one(source, output, "wav")

            self.assertTrue(result.success)
            self.assertEqual(result.output_path, output)

    @patch("app.converter.subprocess.run")
    def test_convert_one_supports_encrypted_audio(self, run_mock) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "a.ncm"
            output = root / "b.mp3"
            decrypted_dir = root / "decrypt"
            decrypted_dir.mkdir()
            decrypted = decrypted_dir / "temp.mp3"
            source.write_bytes(b"1")
            decrypted.write_bytes(b"2")

            run_mock.side_effect = [
                type("Result", (), {"returncode": 0, "stdout": '{"streams":[{"codec_type":"audio"}]}', "stderr": ""})(),
                type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})(),
            ]

            with patch("app.converter.decrypt_audio_to_temp", return_value=decrypted) as decrypt_mock:
                result = convert_one(source, output, "mp3")

            self.assertTrue(result.success)
            self.assertEqual(result.output_path, output)
            decrypt_mock.assert_called_once_with(source)
            ffmpeg_args = run_mock.call_args_list[1][0][0]
            self.assertEqual(ffmpeg_args[3], str(decrypted))
            self.assertFalse(decrypted.exists())
            self.assertFalse(decrypted_dir.exists())

    def test_convert_one_reports_decrypt_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "bad.kgm"
            output = root / "bad.mp3"
            source.write_bytes(b"bad")

            with patch("app.converter.decrypt_audio_to_temp", side_effect=DecryptError("文件解密失败")):
                result = convert_one(source, output, "mp3")

            self.assertFalse(result.success)
            self.assertEqual(result.message, "解密失败，请检查文件是否受支持")

    @patch("app.converter.subprocess.run")
    def test_convert_one_cleans_temp_file_when_probe_fails(self, run_mock) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "a.kgm"
            output = root / "b.mp3"
            decrypted_dir = root / "decrypt"
            decrypted_dir.mkdir()
            decrypted = decrypted_dir / "temp.mp3"
            source.write_bytes(b"1")
            decrypted.write_bytes(b"2")
            run_mock.return_value = type("Result", (), {"returncode": 1, "stdout": "", "stderr": "probe failed"})()

            with patch("app.converter.decrypt_audio_to_temp", return_value=decrypted):
                result = convert_one(source, output, "mp3")

            self.assertFalse(result.success)
            self.assertEqual(result.message, "probe failed")
            self.assertFalse(decrypted.exists())
            self.assertFalse(decrypted_dir.exists())

    @patch("app.converter.convert_one")
    def test_convert_many_keeps_relative_path(self, convert_one_mock) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_dir = root / "out"
            item = SourceItem(source_path=root / "a.mp3", relative_path=Path("a") / "b.mp3")
            convert_one_mock.return_value = type("R", (), {"success": True})()

            convert_many([item], output_dir, "ogg")

            args = convert_one_mock.call_args[0]
            self.assertEqual(args[1], output_dir / "a" / "b.ogg")


if __name__ == "__main__":
    unittest.main()
