"""Application errors and file logging for the authentication demo."""

import logging
from pathlib import Path


class UserInputError(ValueError):
    """A validation or authentication error safe to show to the user."""


class DataStoreError(RuntimeError):
    """A storage error with a safe, user-facing message."""


def configure_logging():
    log_path = Path("lab10/logs/application.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        encoding="utf-8",
        force=True,
    )


logger = logging.getLogger("lab10")
