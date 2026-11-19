"""Small SQLite persistence layer for the Week 10 authentication demo."""

import sqlite3
from contextlib import closing
from pathlib import Path

from lab10.errors import DataStoreError, UserInputError, logger


class Database:
    def __init__(self, path="lab10/authentication.db"):
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self):
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self):
        with closing(self.connect()) as connection, connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS login_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    success INTEGER NOT NULL CHECK (success IN (0, 1)),
                    attempted_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
                )
            """)

    def create_user(self, username, email, password_hash):
        try:
            with closing(self.connect()) as connection, connection:
                cursor = connection.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, password_hash),
                )
                return dict(connection.execute(
                    "SELECT id, username, email, created_at FROM users WHERE id = ?",
                    (cursor.lastrowid,),
                ).fetchone())
        except sqlite3.IntegrityError as error:
            raise UserInputError("Хэрэглэгчийн нэр эсвэл имэйл бүртгэлтэй байна.") from error
        except sqlite3.Error as error:
            logger.exception("SQLite failed while creating a user")
            raise DataStoreError("Бүртгэл хадгалахад мэдээллийн сангийн алдаа гарлаа.") from error

    def get_user_for_login(self, username):
        try:
            with closing(self.connect()) as connection, connection:
                row = connection.execute(
                    "SELECT id, username, email, password_hash, created_at FROM users WHERE username = ? COLLATE NOCASE",
                    (username,),
                ).fetchone()
                return dict(row) if row else None
        except sqlite3.Error as error:
            logger.exception("SQLite failed while looking up a user")
            raise DataStoreError("Хэрэглэгч хайхад мэдээллийн сангийн алдаа гарлаа.") from error

    def record_login(self, username, success):
        try:
            with closing(self.connect()) as connection, connection:
                connection.execute(
                    "INSERT INTO login_history (username, success) VALUES (?, ?)",
                    (username, int(success)),
                )
        except sqlite3.Error as error:
            logger.exception("SQLite failed while recording login history")
            raise DataStoreError("Нэвтрэх түүх хадгалахад мэдээллийн сангийн алдаа гарлаа.") from error

    def get_login_history(self, username, limit=20):
        try:
            with closing(self.connect()) as connection, connection:
                rows = connection.execute(
                    "SELECT username, success, attempted_at FROM login_history "
                    "WHERE username = ? COLLATE NOCASE ORDER BY id DESC LIMIT ?",
                    (username, limit),
                ).fetchall()
                return [dict(row) for row in rows]
        except sqlite3.Error as error:
            logger.exception("SQLite failed while reading login history")
            raise DataStoreError("Нэвтрэх түүх уншихад мэдээллийн сангийн алдаа гарлаа.") from error
