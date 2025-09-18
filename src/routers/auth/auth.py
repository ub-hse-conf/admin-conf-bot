from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from structlog import get_logger

from src.constants.messages import WRONG_CODE_COMMAND_EXCEPTION, WRONG_CODE_EXCEPTION, SUCCESSFUL_AUTH_TEXT
from src.routers.menu import generate_menu_keyboard
from src.services import AuthService

router = Router()

@router.message(Command("auth"))
async def auth(message: Message, command: CommandObject, auth_service: AuthService):
    if command.args is None:
        await message.answer(WRONG_CODE_COMMAND_EXCEPTION)
        get_logger().warn("Handled auth command with no payload")
        return

    code = command.args.strip()
    get_logger().info("Handled auth command with payload: %s", command.args)

    authenticated = await auth_service.auth(message.chat.id, code)
    if not authenticated:
        get_logger().warn("Auth failed for chat %s with code %s", message.chat.id, code)
        await message.answer(WRONG_CODE_EXCEPTION)
        return

    await message.answer(SUCCESSFUL_AUTH_TEXT, reply_markup=generate_menu_keyboard())

