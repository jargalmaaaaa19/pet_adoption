"""CLI integration test for login, private history, logout, and exit."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from lab10.auth import AuthService
from lab10.database import Database
from lab10.main import run_menu


class MenuIntegrationTests(unittest.TestCase):
    def test_user_can_log_out_and_history_requires_a_session(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            auth = AuthService(Database(Path(temp_dir) / "cli.db"))
            auth.register("naraa", "naraa@example.com", "secure-pass-1")
            inputs = ["1", "naraa", "secure-pass-1", "3", "4", "3", "5"]
            output = io.StringIO()
            with patch("lab10.main.prompt", side_effect=inputs), redirect_stdout(output):
                run_menu(auth)

        transcript = output.getvalue()
        self.assertIn("Тавтай морил, naraa!", transcript)
        self.assertIn("Нэвтрэх түүх:", transcript)
        self.assertIn("naraa хэрэглэгчээс амжилттай гарлаа.", transcript)
        self.assertIn("Нэвтрэх түүхээ харахын тулд эхлээд нэвтэрнэ үү.", transcript)
        self.assertIn("Төлөв: Нэвтрээгүй", transcript)


if __name__ == "__main__":
    unittest.main()
