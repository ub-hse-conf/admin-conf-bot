import asyncio
import uuid

from aiogram import Dispatcher

from src import routers, middlewares, api, custom_logging
from src.api import endpoint, UserClient, AuthClient
from src.api.client import ActivityClient, TaskClient, ConferenceClient
from src.bot import CustomBot
from src.config import BOT_TOKEN, SERVER_URL, USERNAME_API, PASSWORD_API
from src.services import AuthService, ActivityService, TaskService
from src.storage import create_bot_storage
from src.version import get_version


async def main():
    instance_id = str(uuid.uuid4())
    version = get_version()

    custom_logging.init_logging(instance_id, version)

    storage = create_bot_storage()

    user_client = UserClient(base_url=SERVER_URL, username=USERNAME_API, password=PASSWORD_API)
    auth_client = AuthClient(base_url=SERVER_URL, username=USERNAME_API, password=PASSWORD_API)
    activity_client = ActivityClient(base_url=SERVER_URL, username=USERNAME_API, password=PASSWORD_API)
    task_client = TaskClient(base_url=SERVER_URL, username=USERNAME_API, password=PASSWORD_API)
    conference_client = ConferenceClient(base_url=SERVER_URL, username=USERNAME_API, password=PASSWORD_API)

    auth_service = AuthService(auth_client, user_client, storage)
    activity_service = ActivityService(activity_client)
    task_service = TaskService(task_client)

    bot = CustomBot.create(BOT_TOKEN, storage, auth_service)
    await routers.register_commands_info(bot)

    dp = Dispatcher(storage=storage, auth_service=auth_service, activity_service=activity_service,
                    task_service=task_service, conference_client=conference_client)

    app = api.create_app_instance(bot)
    endpoint.register_endpoints(app)

    middlewares.register_middlewares(dp)
    routers.register_routes(dp)

    async with bot:
        await asyncio.gather(
            bot.start(dp),
            api.start_web(app, dp, bot)
        )