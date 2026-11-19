"""Run integration tests first, then start the Week 10 terminal application."""

import unittest

from lab10.auth import AuthService
from lab10.database import Database
from lab10.errors import DataStoreError, UserInputError, configure_logging, logger


def run_integration_tests():
    suite = unittest.defaultTestLoader.discover("lab10/tests")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()


def prompt(label, secret=False):
    try:
        if secret:
            from getpass import getpass
            return getpass(label)
        return input(label)
    except (EOFError, KeyboardInterrupt):
        print("\nОролт цуцлагдлаа.")
        return None


def show_history(auth, username):
    history = auth.login_history(username)
    print("\nНэвтрэх түүх:")
    if not history:
        print("  Түүх одоогоор алга.")
    for entry in history:
        status = "Амжилттай" if entry["success"] else "Амжилтгүй"
        print(f"  {entry['attempted_at']} | {status}")


def run_menu(auth=None):
    auth = auth or AuthService(Database())
    current_user = None
    print("\n=== Амьтан үрчлэлтийн систем | Week 10 ===")
    while True:
        session_name = current_user["username"] if current_user else "Нэвтрээгүй"
        print(f"\nТөлөв: {session_name}")
        print("1. Нэвтрэх\n2. Бүртгүүлэх\n3. Миний нэвтрэх түүх\n4. Системээс гарах\n5. Программаас гарах")
        choice = prompt("Сонголт: ")
        if choice is None or choice == "5":
            print("Программаас гарлаа.")
            return
        try:
            if choice == "1":
                username = prompt("Хэрэглэгчийн нэр: ")
                password = prompt("Нууц үг: ", secret=True)
                if username is None or password is None:
                    continue
                current_user = auth.login(username, password)
                print(f"Тавтай морил, {current_user['username']}!")
            elif choice == "2":
                username = prompt("Хэрэглэгчийн нэр: ")
                email = prompt("Имэйл: ")
                password = prompt("Нууц үг: ", secret=True)
                if None in (username, email, password):
                    continue
                auth.register(username, email, password)
                print("Бүртгэл амжилттай. Одоо нэвтэрч болно.")
            elif choice == "3":
                if current_user is None:
                    print("Нэвтрэх түүхээ харахын тулд эхлээд нэвтэрнэ үү.")
                else:
                    show_history(auth, current_user["username"])
            elif choice == "4":
                if current_user is None:
                    print("Та одоогоор нэвтрээгүй байна.")
                else:
                    print(f"{current_user['username']} хэрэглэгчээс амжилттай гарлаа.")
                    current_user = None
            else:
                print("Сонголт буруу байна. 1-5-ийн аль нэгийг сонгоно уу.")
        except (UserInputError, DataStoreError) as error:
            logger.warning("Request rejected: %s", error)
            print(f"Алдаа: {error}")
        except Exception:
            logger.exception("Unexpected error in the command-line application")
            print("Алдаа: Системд гэнэтийн алдаа гарлаа. Дахин оролдоно уу.")


def main():
    configure_logging()
    print("Интеграцийн тестүүдийг ажиллуулж байна...\n")
    if not run_integration_tests():
        print("Тест амжилтгүй. Үндсэн цэсийг эхлүүлсэнгүй.")
        return 1
    print("\nБүх интеграцийн тест амжилттай. Үндсэн цэсийг эхлүүлж байна.")
    run_menu()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
