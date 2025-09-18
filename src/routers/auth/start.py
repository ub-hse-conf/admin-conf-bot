from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from structlog import get_logger

from src.constants.messages import WELCOME_TEXT, SUCCESSFUL_AUTH_TEXT
from src.routers.menu import generate_menu_keyboard
from src.services import AuthService

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, auth_service: AuthService):
    get_logger().info("Handled start command")

    if not await auth_service.is_authenticated(message.from_user.id):
        await message.answer(WELCOME_TEXT)
        return

    get_logger().info("User already authenticated")
    await message.answer(SUCCESSFUL_AUTH_TEXT, reply_markup=generate_menu_keyboard())
