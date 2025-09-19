from src.api.client.base_client import BaseClient
from src.models import Error, ActivityEventStatus


class ActivityClient(BaseClient):
    async def get_activities(self) -> list[dict] | Error:
        url = f"/activities"
        client: ActivityClient
        async with self as client:
            return await client._get_request_or_error(url)

    async def get_activity(self, activity_id: int) -> dict | Error:
        url = f"/activities/{activity_id}"
        client: ActivityClient
        async with self as client:
            return await client._get_request_or_error(url)

    async def get_activity_event(self, activity_id: int) -> dict | Error:
        url = f"/activities/{activity_id}/event"
        client: ActivityClient
        async with self as client:
            return await client._get_request_or_error(url)

    async def copy_activity_visits(self, from_activity_id: int, to_activity_id: int) -> None | Error:
        url = f"/activities/{from_activity_id}/visits-copy/{to_activity_id}"
        client: ActivityClient
        async with self as client:
            return await client._post_request_or_error(url)

    async def change_activity_event_status(self, activity_id: int, activity_status: ActivityEventStatus) -> None | Error:
        url = f"/activities/{activity_id}/event/status"
        status = {
            ActivityEventStatus.CONTINUED: "RUN",
            ActivityEventStatus.ENDED: "END",
        }

        client: ActivityClient
        async with self as client:
            return await client._post_request_or_error(url, {"status": status[activity_status]})
