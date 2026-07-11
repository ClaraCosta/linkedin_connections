from __future__ import annotations

import logging
import socket
import subprocess
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver

from config import settings


class ChromeBrowser:
    """Inicia o Chrome com perfil persistente e anexa o Selenium a ele."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.driver: WebDriver | None = None

    def start(self) -> WebDriver:
        Path(settings.CHROMEDRIVER_LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
        self._stop_existing_chrome()
        self._clear_profile_locks()
        self._launch_chrome()
        self._wait_for_debugger()

        options = Options()
        options.binary_location = settings.CHROME_BINARY
        options.debugger_address = settings.CHROME_DEBUGGER_ADDRESS
        self.driver = webdriver.Chrome(
            service=Service(log_output=settings.CHROMEDRIVER_LOG_PATH),
            options=options,
        )
        self.logger.info("Chrome conectado em %s", settings.CHROME_DEBUGGER_ADDRESS)
        return self.driver

    def close(self) -> None:
        if self.driver is not None:
            self.driver.quit()
            self.driver = None

    def _stop_existing_chrome(self) -> None:
        self.logger.info("Encerrando instancias anteriores do Chrome")
        subprocess.run(["pkill", "chrome"], check=False, capture_output=True)

    def _clear_profile_locks(self) -> None:
        settings.CHROME_USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
        for lock_name in ("SingletonLock", "SingletonCookie", "SingletonSocket"):
            (settings.CHROME_USER_DATA_DIR / lock_name).unlink(missing_ok=True)

    def _launch_chrome(self) -> None:
        self.logger.info("Abrindo Chrome com perfil em %s", settings.CHROME_USER_DATA_DIR)
        subprocess.Popen(
            [
                settings.CHROME_BINARY,
                "--remote-debugging-port=9222",
                f"--user-data-dir={settings.CHROME_USER_DATA_DIR}",
                "--disable-dev-shm-usage",
                "--headless=new",
                "--disable-gpu",
                "--start-maximized",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _wait_for_debugger(self) -> None:
        host, port = settings.CHROME_DEBUGGER_ADDRESS.rsplit(":", maxsplit=1)
        for _ in range(15):
            try:
                with socket.create_connection((host, int(port)), timeout=1):
                    return
            except OSError:
                time.sleep(1)

        raise RuntimeError(
            f"O Chrome nao respondeu em {settings.CHROME_DEBUGGER_ADDRESS}."
        )
