from src.api.client.base_client import BaseClient
from src.models import Error
from src.utils.mapper import parse_error


class UserClient(BaseClient):
    async def exists_user(self, telegram_id: int) -> bool | Error:
        url = f"/users/{telegram_id}"
        client: UserClient
        async with self as client:
            response = await client._get_request(url)
            if response.status_code == 404:
                return False

            elif response.status_code == 200:
                return True

            return parse_error(response.json())


    async def get_user(self, telegram_id: int) -> dict | Error:
        url = f"/users/{telegram_id}"
        client: UserClient
        async with self as client:
            return await client._get_request_or_error(url)

    async def create_user(self, telegram_id: int) -> dict | Error:
        url = f"/users"
        payload = {
            "tgId": telegram_id,
            "fullName": "Волонтёр",
            "course": 10,
            "program": "Волонтёры"
        }

        client: UserClient
        async with self as client:
            return await client._post_request_or_error(url, payload)
