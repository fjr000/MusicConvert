import unittest
from unittest.mock import patch

from app.subprocess_utils import hidden_subprocess_kwargs


class SubprocessUtilsTestCase(unittest.TestCase):
    def test_hidden_subprocess_kwargs_returns_empty_on_non_windows(self) -> None:
        with patch("app.subprocess_utils.os.name", "posix"):
            self.assertEqual(hidden_subprocess_kwargs(), {})

    def test_hidden_subprocess_kwargs_uses_create_no_window_on_windows(self) -> None:
        with patch("app.subprocess_utils.os.name", "nt"), patch(
            "app.subprocess_utils.subprocess.CREATE_NO_WINDOW",
            134217728,
            create=True,
        ):
            self.assertEqual(hidden_subprocess_kwargs(), {"creationflags": 134217728})


if __name__ == "__main__":
    unittest.main()
