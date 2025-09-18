from aiogram import BaseMiddleware
from aiogram.types import Message

from src.bot import CustomBot
from src.constants.messages import FORBIDDEN_EXCEPTION


class ExcludedCommandsFilter:
    def __init__(self, excluded_commands: list):
        self.excluded_commands = excluded_commands

    async def __call__(self, message: Message) -> bool:
        if not message.text or not message.text.startswith('/'):
            return True

        command = message.text.split()[0][1:].split('@')[0]
        return command not in self.excluded_commands

class SecurityMiddleware(BaseMiddleware):
    def __init__(self):
        self.excluded_commands = ['start', 'auth']

    async def __call__(self, handler, event, data):
        if event.message is None:
            return await handler(event, data)

        message = event.message
        filter_check = ExcludedCommandsFilter(self.excluded_commands)
        should_check = await filter_check(message)

        if not should_check:
            return await handler(event, data)

        bot: CustomBot = event.bot
        auth_service = bot.get_auth_service()
        id = message.from_user.id

        if not await auth_service.is_authenticated(id):
            await message.answer(FORBIDDEN_EXCEPTION)
            return

        return await handler(event, data)
