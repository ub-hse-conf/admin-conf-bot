from structlog import get_logger

from src.api import UserClient, AuthClient
from src.models import Error, UserRole, ErrorType
from src.storage import BaseStorage


class AuthService:
    def __init__(self, auth_client: AuthClient, user_client: UserClient, storage: BaseStorage):
        self.auth_client = auth_client
        self.user_client = user_client
        self.storage = storage

    async def generate_codes(self, count: int) -> list[str]:
        return await self.auth_client.generate_codes(count)

    async def is_authenticated(self, telegram_id: int) -> bool:
        cache_key = f"auth:{telegram_id}"
        if await self.storage.get(cache_key) is not None:
            if await self.storage.get(cache_key) == "true":
                get_logger().info(f"Cached authentication for {telegram_id}")
                return True


        user = await self.user_client.get_user(telegram_id)
        if isinstance(user, Error):
            get_logger().warn(f"Not authenticated for {user}")
            return False

        role = UserRole[user["role"]]

        if role == UserRole.ADMIN or role == UserRole.VOLUNTEER:
            get_logger().info(f"Granted access by {role.value}")
            await self.storage.set(cache_key, "true")
            return True

        get_logger().info(f"Not granted access by {role.value}")
        return False

    async def is_admin(self, telegram_id: int) -> bool:
        cache_key = f"admin_auth:{telegram_id}"
        if await self.storage.get(cache_key) is not None:
            if await self.storage.get(cache_key) == "true":
                get_logger().info(f"Cached admin authentication for {telegram_id}")
                return True

        user = await self.user_client.get_user(telegram_id)

        if isinstance(user, Error):
            return False

        role = UserRole[user["role"]]

        if role == UserRole.ADMIN:
            await self.storage.set(cache_key, "true")
            return True

        return False

    async def auth(self, telegram_id: int, code: str) -> bool:
        if await self.is_authenticated(telegram_id):
            return True

        result = await self.auth_client.auth_by_code(telegram_id, code)

        if isinstance(result, Error):
            if result.error_type == ErrorType.USER_NOT_FOUND:
                get_logger().info(f"User not found, creating new user")
                await self.user_client.create_user(telegram_id)
                await self.auth(telegram_id, code)
            elif result.error_type == ErrorType.AUTHCODE_NOT_FOUND:
                get_logger().warn(f"Auth code {code} not found")
                return False
            else:
                get_logger().warn(f"Invalid response from auth service: {result}")
                return False

        return result