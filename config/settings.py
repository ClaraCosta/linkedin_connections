"""Runtime settings for the LinkedIn connection RPA.

Edit this file when you need to change how the command behaves.
Environment variables with the same names take precedence.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from config.constants import (
    DEFAULT_DAILY_CONNECTION_LIMIT,
    DEFAULT_BATCH_SIZE,
    DEFAULT_MAX_BATCH_PAUSE_SECONDS,
    DEFAULT_MAX_INVITATION_PAUSE_SECONDS,
    DEFAULT_MAX_PAGE_REFRESHES_WITHOUT_SUGGESTIONS,
    DEFAULT_MIN_BATCH_PAUSE_SECONDS,
    DEFAULT_MIN_INVITATION_PAUSE_SECONDS,
    DEFAULT_SCROLL_PAUSE_SECONDS,
    DEFAULT_WAIT_SECONDS,
    GOOGLE_CHROME_BINARY,
)


PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / ".env")


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "sim", "s"}


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default

    return int(value)


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default

    return float(value)


DAILY_CONNECTION_LIMIT = _get_int(
    "DAILY_CONNECTION_LIMIT",
    DEFAULT_DAILY_CONNECTION_LIMIT,
)

WAIT_SECONDS = _get_int("WAIT_SECONDS", DEFAULT_WAIT_SECONDS)
SCROLL_PAUSE_SECONDS = _get_float(
    "SCROLL_PAUSE_SECONDS",
    DEFAULT_SCROLL_PAUSE_SECONDS,
)
MIN_INVITATION_PAUSE_SECONDS = _get_float(
    "MIN_INVITATION_PAUSE_SECONDS",
    DEFAULT_MIN_INVITATION_PAUSE_SECONDS,
)
MAX_INVITATION_PAUSE_SECONDS = max(
    MIN_INVITATION_PAUSE_SECONDS,
    _get_float("MAX_INVITATION_PAUSE_SECONDS", DEFAULT_MAX_INVITATION_PAUSE_SECONDS),
)
BATCH_SIZE = max(1, _get_int("BATCH_SIZE", DEFAULT_BATCH_SIZE))
MIN_BATCH_PAUSE_SECONDS = _get_float(
    "MIN_BATCH_PAUSE_SECONDS",
    DEFAULT_MIN_BATCH_PAUSE_SECONDS,
)
MAX_BATCH_PAUSE_SECONDS = max(
    MIN_BATCH_PAUSE_SECONDS,
    _get_float("MAX_BATCH_PAUSE_SECONDS", DEFAULT_MAX_BATCH_PAUSE_SECONDS),
)
MAX_PAGE_REFRESHES_WITHOUT_SUGGESTIONS = max(
    0,
    _get_int(
        "MAX_PAGE_REFRESHES_WITHOUT_SUGGESTIONS",
        DEFAULT_MAX_PAGE_REFRESHES_WITHOUT_SUGGESTIONS,
    ),
)

CHROME_BINARY = os.getenv("CHROME_BINARY", GOOGLE_CHROME_BINARY)
CHROME_USER_DATA_DIR = Path(
    os.getenv("CHROME_USER_DATA_DIR", str(Path.home() / ".linkedin-selenium"))
)
CHROME_DEBUGGER_ADDRESS = os.getenv("CHROME_DEBUGGER_ADDRESS", "127.0.0.1:9222")
CHROMEDRIVER_LOG_PATH = os.getenv("CHROMEDRIVER_LOG_PATH", str(PROJECT_DIR / "logs" / "chromedriver.log"))
OUTPUT_XLSX_PATH = os.getenv(
    "OUTPUT_XLSX_PATH",
    str(Path.home() / "Documentos" / "linkedin_connections.xlsx"),
)
LOG_DIR = Path(os.getenv("LOG_DIR", str(PROJECT_DIR / "logs")))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
START_MAXIMIZED = _get_bool("START_MAXIMIZED", True)
DRY_RUN = _get_bool("DRY_RUN", False)
KEEP_BROWSER_OPEN = _get_bool("KEEP_BROWSER_OPEN", True)
