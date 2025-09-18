__all__ = [
    "register_routes",
    "register_commands_info"
]

from aiogram import Dispatcher, Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand, BotCommandScopeDefault, CallbackQuery

from src.routers import scanner, activity, management, be_real
from src.routers.auth import start, auth

router = Router()

@router.callback_query(F.data == "CANCEL")
async def cancel_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Действите отменено")
    await state.clear()
    await callback.message.delete()


def register_routes(dp: Dispatcher):
    dp.include_router(router)
    dp.include_router(start.router)
    dp.include_router(auth.router)
    dp.include_router(scanner.router)
    dp.include_router(activity.router)
    dp.include_router(be_real.router)
    dp.include_router(management.router)


async def register_commands_info(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command='/scanner', description='Запустить сканер'),
            BotCommand(command='/auth', description='Авторизоваться в боте'),
            BotCommand(command='/activity', description='Управление активностями'),
            BotCommand(command="/be_real", description="Управление BeReal"),
            BotCommand(command="/manage", description="Управление конференцией"),
        ],
        scope=BotCommandScopeDefault()
    )
