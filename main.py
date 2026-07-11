from __future__ import annotations

import logging
import sys

from selenium.common.exceptions import WebDriverException

from config import settings
from src.bot import ConnectionBot
from src.browser import ChromeBrowser
from src.linkedin import LinkedInClient
from src.logging_config import configure_logging
from src.storage import ConnectionWorkbook


def main() -> int:
    log_path = configure_logging(settings.LOG_DIR, settings.LOG_LEVEL)
    logger = logging.getLogger("main")
    logger.info("Inicio da execucao. Log: %s", log_path)
    browser = ChromeBrowser()

    try:
        driver = browser.start()
        bot = ConnectionBot(LinkedInClient(driver), ConnectionWorkbook(settings.OUTPUT_XLSX_PATH))
        stats = bot.run()
        action = "perfil(is) simulado(s)" if settings.DRY_RUN else "convite(s) enviado(s)"
        logger.info("Finalizado: %s %s, %s botao(oes) pulado(s).", stats.clicked, action, stats.skipped)
        return 0
    except (RuntimeError, WebDriverException):
        logger.exception("Falha durante a execucao do bot")
        return 1
    finally:
        if not settings.KEEP_BROWSER_OPEN:
            browser.close()


if __name__ == "__main__":
    raise SystemExit(main())
