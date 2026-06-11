"""Integration tests for encrypted audio format support.

These tests verify that the application correctly handles various encrypted
audio formats by checking file recognition and error handling paths.

Note: These are structural tests only. Real decryption requires actual
encrypted audio files and the musicdecrypto.exe tool.
"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.decryptor import is_encrypted_audio_file


class EncryptedFormatTestCase(unittest.TestCase):
    """Test encrypted audio format detection and handling."""

    def test_ncm_format_detected(self):
        """NCM files should be recognized as encrypted."""
        path = Path("test.ncm")
        self.assertTrue(is_encrypted_audio_file(path))

    def test_qmc_variants_detected(self):
        """QMC format variants should be recognized."""
        variants = [
            "test.qmc0", "test.qmc2", "test.qmc3", "test.qmc4",
            "test.qmc6", "test.qmc8", "test.qmcogg", "test.qmcflac",
            "test.qmc999",  # Extended variant
        ]
        for variant in variants:
            path = Path(variant)
            with self.subTest(format=variant):
                self.assertTrue(is_encrypted_audio_file(path))

    def test_kgm_formats_detected(self):
        """KGM and related formats should be recognized."""
        formats = ["test.kgm", "test.kgma", "test.vpr"]
        for fmt in formats:
            path = Path(fmt)
            with self.subTest(format=fmt):
                self.assertTrue(is_encrypted_audio_file(path))

    def test_tm_formats_detected(self):
        """Tencent music formats should be recognized."""
        formats = ["test.tm2", "test.tm6"]
        for fmt in formats:
            path = Path(fmt)
            with self.subTest(format=fmt):
                self.assertTrue(is_encrypted_audio_file(path))

    def test_bkc_formats_detected(self):
        """BKC (backup) formats should be recognized."""
        formats = [
            "test.bkcmp3", "test.bkcm4a", "test.bkcwma",
            "test.bkcogg", "test.bkcwav", "test.bkcape", "test.bkcflac"
        ]
        for fmt in formats:
            path = Path(fmt)
            with self.subTest(format=fmt):
                self.assertTrue(is_encrypted_audio_file(path))

    def test_mgg_formats_detected(self):
        """MGG (Migu) formats should be recognized."""
        formats = ["test.mgg", "test.mgg1", "test.mggl", "test.mflac", "test.mflac0", "test.mmp4"]
        for fmt in formats:
            path = Path(fmt)
            with self.subTest(format=fmt):
                self.assertTrue(is_encrypted_audio_file(path))

    def test_hex_formats_detected(self):
        """Hex-named encrypted formats should be recognized."""
        formats = ["test.6d7033", "test.6d3461", "test.6f6767", "test.776176", "test.666c6163"]
        for fmt in formats:
            path = Path(fmt)
            with self.subTest(format=fmt):
                self.assertTrue(is_encrypted_audio_file(path))

    def test_kwm_xm_formats_detected(self):
        """KWM and XM formats should be recognized."""
        formats = ["test.kwm", "test.x2m", "test.x3m", "test.xm"]
        for fmt in formats:
            path = Path(fmt)
            with self.subTest(format=fmt):
                self.assertTrue(is_encrypted_audio_file(path))

    def test_plain_audio_not_detected_as_encrypted(self):
        """Plain audio formats should not be detected as encrypted."""
        plain_formats = ["test.mp3", "test.flac", "test.wav", "test.m4a", "test.ogg"]
        for fmt in plain_formats:
            path = Path(fmt)
            with self.subTest(format=fmt):
                self.assertFalse(is_encrypted_audio_file(path))

    def test_case_insensitive_detection(self):
        """Format detection should be case-insensitive."""
        self.assertTrue(is_encrypted_audio_file(Path("TEST.NCM")))
        self.assertTrue(is_encrypted_audio_file(Path("Test.Qmc0")))
        self.assertTrue(is_encrypted_audio_file(Path("TeSt.KGM")))


if __name__ == "__main__":
    unittest.main()
