"""Authentication rules kept separate from the command-line interface."""

import hashlib
import hmac
import re
import secrets

from lab10.errors import UserInputError


class AuthService:
    ITERATIONS = 240_000

    def __init__(self, database):
        self.database = database

    @classmethod
    def _hash_password(cls, password, salt=None):
        salt = salt or secrets.token_hex(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt), cls.ITERATIONS
        ).hex()
        return f"{salt}${digest}"

    @classmethod
    def _password_matches(cls, password, stored_hash):
        try:
            salt, expected = stored_hash.split("$", 1)
            actual = cls._hash_password(password, salt).split("$", 1)[1]
            return hmac.compare_digest(actual, expected)
        except (ValueError, TypeError):
            return False

    def register(self, username, email, password):
        username, email = username.strip(), email.strip()
        if len(username) < 3:
            raise UserInputError("Хэрэглэгчийн нэр хамгийн багадаа 3 тэмдэгт байна.")
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            raise UserInputError("Зөв имэйл хаяг оруулна уу.")
        if len(password) < 8:
            raise UserInputError("Нууц үг хамгийн багадаа 8 тэмдэгт байна.")
        return self.database.create_user(username, email, self._hash_password(password))

    def login(self, username, password):
        username = username.strip()
        user = self.database.get_user_for_login(username) if username else None
        success = bool(user and self._password_matches(password, user["password_hash"]))
        self.database.record_login(username or "(хоосон)", success)
        if not success:
            raise UserInputError("Хэрэглэгчийн нэр эсвэл нууц үг буруу байна.")
        return {key: user[key] for key in ("id", "username", "email", "created_at")}

    def login_history(self, username):
        return self.database.get_login_history(username)
