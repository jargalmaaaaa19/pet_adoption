"""Integration tests cover the authentication service and real SQLite storage."""

import tempfile
import unittest
from pathlib import Path

from lab10.auth import AuthService
from lab10.database import Database


class AuthenticationIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "test-auth.db"
        self.database = Database(self.database_path)
        self.auth = AuthService(self.database)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_register_login_and_history_survive_database_reopen(self):
        self.auth.register("naraa", "naraa@example.com", "secure-pass-1")
        user = self.auth.login("naraa", "secure-pass-1")
        self.assertEqual(user["username"], "naraa")
        self.database = Database(self.database_path)
        history = AuthService(self.database).login_history("naraa")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["success"], 1)

    def test_failed_login_is_recorded(self):
        self.auth.register("bold", "bold@example.com", "secure-pass-2")
        with self.assertRaisesRegex(ValueError, "буруу"):
            self.auth.login("bold", "incorrect")
        self.assertEqual(self.auth.login_history("bold")[0]["success"], 0)

    def test_duplicate_username_or_email_is_rejected(self):
        self.auth.register("saraa", "saraa@example.com", "secure-pass-3")
        with self.assertRaisesRegex(ValueError, "бүртгэлтэй"):
            self.auth.register("SARAA", "other@example.com", "secure-pass-4")
        with self.assertRaisesRegex(ValueError, "бүртгэлтэй"):
            self.auth.register("another", "saraa@example.com", "secure-pass-4")

    def test_registration_validates_fields(self):
        for args in (("ab", "a@example.com", "secure-pass"),
                     ("valid", "not-an-email", "secure-pass"),
                     ("valid", "v@example.com", "short")):
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.auth.register(*args)

    def test_password_is_not_stored_as_plaintext(self):
        self.auth.register("tsetseg", "tsetseg@example.com", "secure-pass-5")
        stored = self.database.get_user_for_login("tsetseg")["password_hash"]
        self.assertNotIn("secure-pass-5", stored)
        self.assertIn("$", stored)

    def test_login_history_is_isolated_by_username(self):
        self.auth.register("oneuser", "one@example.com", "secure-pass-6")
        self.auth.register("twouser", "two@example.com", "secure-pass-7")
        self.auth.login("oneuser", "secure-pass-6")
        self.assertEqual(self.auth.login_history("twouser"), [])


if __name__ == "__main__":
    unittest.main()
