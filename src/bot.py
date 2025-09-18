from typing import Any

from structlog import get_logger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.config import WORKING_MODE, WEBHOOK_URL, WEBHOOK_PATH
from src.models import WorkingMode
from src.services import AuthService
from src.storage import BaseStorage


class CustomBot(Bot):
    logger: Any

    @staticmethod
    def create(token: str, storage: BaseStorage, auth_service: AuthService):
        return CustomBot(
            token=token,
            storage=storage,
            default=DefaultBotProperties(parse_mode="Markdown"),
            auth_service=auth_service
        )

    def __init__(
            self,
            token,
            storage: BaseStorage,
            auth_service: AuthService,
            *args,
            **kwargs,
    ):
        super().__init__(token, *args, **kwargs)
        self._storage = storage
        self._auth_service = auth_service
        self.logger = get_logger(__name__)


    @property
    def storage(self) -> BaseStorage:
        return self._storage

    def get_auth_service(self) -> AuthService:
        return self._auth_service

    async def start(self, dp: Dispatcher):
        if WORKING_MODE == WorkingMode.LONG_POLLING:
            self.logger.info("Bot has started pulling")
            await dp.start_polling(self)
        else:
            if not WEBHOOK_URL:
                raise RuntimeError("WEBHOOK_URL must be set")

            webhook_info = await self.get_webhook_info()

            if webhook_info.url != WEBHOOK_URL + WEBHOOK_PATH:
                await self.delete_webhook()

                await self.set_webhook(
                    url=WEBHOOK_URL + WEBHOOK_PATH,
                    drop_pending_updates=False
                )
                self.logger.info("Webhook URL changed to %s", WEBHOOK_URL + WEBHOOK_PATH)

            self.logger.info("Webhook linked to bot")