from src.api.client.base_client import BaseClient
from src.models import Error
from src.utils.mapper import parse_error


class AuthClient(BaseClient):
    async def auth_by_code(self, telegram_id: int, code: str) -> bool | Error:
        url = f"/auth/code/activate"
        client: AuthClient
        async with self as client:
            response = await client._post_request(url, payload={"code": code, "tgId": telegram_id})
            if response.status_code == 400:
                return False

            elif response.status_code == 200:
                return True

            return parse_error(response.json())

    async def generate_codes(self, count: int) -> list[str] | Error:
        url = f"/auth/code/generate"
        client: AuthClient

        async with self as client:
            response = await client._post_request_or_error(url, payload={"count": count, "type": "VOLUNTEER"})
            return response

