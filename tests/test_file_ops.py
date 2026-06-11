import tempfile
import unittest
from pathlib import Path

from app.file_ops import (
    build_output_path,
    collect_file_items,
    collect_folder_items,
    make_unique_path,
)


class FileOpsTestCase(unittest.TestCase):
    def test_collect_file_items_filters_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ok_file = root / "a.mp3"
            bad_file = root / "a.txt"
            ok_file.write_bytes(b"1")
            bad_file.write_bytes(b"1")

            items = collect_file_items([str(ok_file), str(bad_file)])

            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].source_path, ok_file)

    def test_collect_folder_items_keeps_relative_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            nested = root / "x" / "y"
            nested.mkdir(parents=True)
            target = nested / "a.flac"
            target.write_bytes(b"1")

            items = collect_folder_items(str(root))

            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].relative_path, Path("x") / "y" / "a.flac")

    def test_collect_file_items_skips_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            missing = root / "missing.mp3"

            items = collect_file_items([str(missing)])

            self.assertEqual(items, [])

    def test_collect_file_items_accepts_encrypted_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            encrypted = root / "a.mflac"
            encrypted.write_bytes(b"1")

            items = collect_file_items([str(encrypted)])

            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].source_path, encrypted)

    def test_collect_folder_items_skips_unsupported_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            nested = root / "x"
            nested.mkdir()
            (nested / "a.txt").write_bytes(b"1")

            items = collect_folder_items(str(root))

            self.assertEqual(items, [])

    def test_collect_folder_items_accepts_qmc_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            nested = root / "x"
            nested.mkdir()
            target = nested / "a.qmc999"
            target.write_bytes(b"1")

            items = collect_folder_items(str(root))

            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].source_path, target)

    def test_build_output_path_and_unique_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output = build_output_path(root, Path("foo") / "bar.mp3", "wav")
            output.write_bytes(b"1")

            unique = make_unique_path(output)

            self.assertEqual(output.name, "bar.wav")
            self.assertEqual(unique.name, "bar_1.wav")


if __name__ == "__main__":
    unittest.main()
