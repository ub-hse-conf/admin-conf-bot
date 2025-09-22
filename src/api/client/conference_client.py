from src.api.client.base_client import BaseClient
from src.exception import ServerErrorException
from src.models import Error
from src.utils.mapper import parse_error


class ConferenceClient(BaseClient):
    async def end_conference(self) -> None | Error:
        url = f"/conference/complete"
        client: ConferenceClient

        async with self as client:
            response = await client._post_request(url)
            if response.is_error:
                error = parse_error(response.json())
                raise ServerErrorException("Error when ending conference", error)

            return None