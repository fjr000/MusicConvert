import unittest
from unittest.mock import patch

from app.subprocess_utils import hidden_subprocess_kwargs


class SubprocessUtilsTestCase(unittest.TestCase):
    def test_hidden_subprocess_kwargs_returns_empty_on_non_windows(self) -> None:
        with patch("app.subprocess_utils.os.name", "posix"):
            self.assertEqual(hidden_subprocess_kwargs(), {})

    def test_hidden_subprocess_kwargs_hides_window_on_windows(self) -> None:
        class FakeStartupInfo:
            def __init__(self) -> None:
                self.dwFlags = 0
                self.wShowWindow = None

        with patch("app.subprocess_utils.os.name", "nt"), patch(
            "app.subprocess_utils.subprocess.CREATE_NO_WINDOW",
            134217728,
            create=True,
        ), patch(
            "app.subprocess_utils.subprocess.STARTUPINFO",
            FakeStartupInfo,
            create=True,
        ), patch(
            "app.subprocess_utils.subprocess.STARTF_USESHOWWINDOW",
            1,
            create=True,
        ), patch(
            "app.subprocess_utils.subprocess.SW_HIDE",
            0,
            create=True,
        ):
            kwargs = hidden_subprocess_kwargs()

        self.assertEqual(kwargs["creationflags"], 134217728)
        startupinfo = kwargs["startupinfo"]
        self.assertEqual(startupinfo.dwFlags, 1)
        self.assertEqual(startupinfo.wShowWindow, 0)


if __name__ == "__main__":
    unittest.main()
