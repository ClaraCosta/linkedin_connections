from __future__ import annotations

import logging
import random
import time

from config import settings
from config.constants import MAX_SCROLL_ATTEMPTS_WITHOUT_CLICK
from src.linkedin import LinkedInClient
from src.models import RunStats
from src.storage import ConnectionWorkbook


class ConnectionBot:
    def __init__(self, linkedin: LinkedInClient, workbook: ConnectionWorkbook) -> None:
        self.linkedin = linkedin
        self.workbook = workbook
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self) -> RunStats:
        self.linkedin.open_suggestions()
        stats = RunStats()
        while stats.clicked < settings.DAILY_CONNECTION_LIMIT:
            buttons = self.linkedin.find_connect_buttons()
            if not buttons:
                stats.scrolls_without_click += 1
                if stats.scrolls_without_click >= MAX_SCROLL_ATTEMPTS_WITHOUT_CLICK:
                    self.logger.info("Nenhuma sugestao encontrada apos %s rolagens", stats.scrolls_without_click)
                    break
                self.linkedin.scroll_for_more_suggestions()
                continue

            stats.scrolls_without_click = 0
            button = buttons[0]
            person = self.linkedin.person_info(button)
            self.logger.info("Tentando conectar: %s - %s", person.name, person.description)
            clicked = self.linkedin.invite(button)
            status = "dry_run" if settings.DRY_RUN else ("pendente_confirmado" if clicked else "nao_confirmado")
            self.workbook.append(person, status)
            if clicked:
                stats.clicked += 1
                action = "Perfis simulados" if settings.DRY_RUN else "Convites confirmados"
                self.logger.info("%s: %s/%s", action, stats.clicked, settings.DAILY_CONNECTION_LIMIT)
                self._wait_after_invitation(stats.clicked)
            else:
                stats.skipped += 1
        return stats

    def _wait_after_invitation(self, invitations_sent: int) -> None:
        if settings.DRY_RUN or invitations_sent >= settings.DAILY_CONNECTION_LIMIT:
            return

        if invitations_sent % settings.BATCH_SIZE == 0:
            seconds = random.uniform(
                settings.MIN_BATCH_PAUSE_SECONDS,
                settings.MAX_BATCH_PAUSE_SECONDS,
            )
            self.logger.info(
                "Lote de %s convites concluido; aguardando %.1f segundos.",
                settings.BATCH_SIZE,
                seconds,
            )
        else:
            seconds = random.uniform(
                settings.MIN_INVITATION_PAUSE_SECONDS,
                settings.MAX_INVITATION_PAUSE_SECONDS,
            )
            self.logger.info("Aguardando %.1f segundos antes do proximo convite.", seconds)

        time.sleep(seconds)
