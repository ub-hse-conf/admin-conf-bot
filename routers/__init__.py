__all__ = [
    "register_routes",
    "register_commands_info"
]

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from routers import scanner


def register_routes(dp: Dispatcher):
    dp.include_router(scanner.router)


async def register_commands_info(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command='/scanner', description='Запустить сканер'),
        ],
        scope=BotCommandScopeDefault()
    )
