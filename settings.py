"""Runtime settings for the LinkedIn connection RPA.

Edit this file when you need to change how the command behaves.
Environment variables with the same names take precedence.
"""

from __future__ import annotations

import os
from pathlib import Path

from consts import (
    DEFAULT_CLICK_PAUSE_SECONDS,
    DEFAULT_DAILY_CONNECTION_LIMIT,
    DEFAULT_SCROLL_PAUSE_SECONDS,
    DEFAULT_WAIT_SECONDS,
    GOOGLE_CHROME_BINARY,
)


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
CLICK_PAUSE_SECONDS = _get_float("CLICK_PAUSE_SECONDS", DEFAULT_CLICK_PAUSE_SECONDS)

PROJECT_DIR = Path(__file__).resolve().parent

CHROME_BINARY = os.getenv("CHROME_BINARY", GOOGLE_CHROME_BINARY)
CHROME_USER_DATA_DIR = os.getenv(
    "CHROME_USER_DATA_DIR",
    str(PROJECT_DIR / ".chrome-profile"),
)
CHROME_PROFILE_DIRECTORY = os.getenv("CHROME_PROFILE_DIRECTORY", "Default")
CHROMEDRIVER_LOG_PATH = os.getenv(
    "CHROMEDRIVER_LOG_PATH",
    str(PROJECT_DIR / "logs" / "chromedriver.log"),
)
OUTPUT_XLSX_PATH = os.getenv(
    "OUTPUT_XLSX_PATH",
    str(Path.home() / "Documentos" / "linkedin_connections.xlsx"),
)
ATTACH_TO_EXISTING_CHROME = _get_bool("ATTACH_TO_EXISTING_CHROME", True)
CHROME_DEBUGGER_ADDRESS = os.getenv("CHROME_DEBUGGER_ADDRESS", "127.0.0.1:9222")

START_MAXIMIZED = _get_bool("START_MAXIMIZED", True)
DRY_RUN = _get_bool("DRY_RUN", False)
KEEP_BROWSER_OPEN = _get_bool("KEEP_BROWSER_OPEN", True)
