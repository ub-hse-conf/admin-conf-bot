from src.api.client import ActivityClient
from src.models import Activity, ActivityEvent, ActivityEventStatus
from src.utils.mapper import parse_activity, parse_activity_event


class ActivityService:
    def __init__(self, activity_client: ActivityClient):
        self.activity_client = activity_client

    async def get_activities(self) -> list[Activity]:
        return list(map(parse_activity, await self.activity_client.get_activities()))

    async def get_activity(self, activity_id: int) -> Activity:
        return parse_activity(await self.activity_client.get_activity(activity_id))

    async def get_activity_event(self, activity_id: int) -> ActivityEvent:
        return parse_activity_event(await self.activity_client.get_activity_event(activity_id))

    async def run_activity_event(self, activity_id: int):
        await self.activity_client.change_activity_event_status(activity_id, ActivityEventStatus.CONTINUED)

    async def stop_activity_event(self, activity_id: int):
        await self.activity_client.change_activity_event_status(activity_id, ActivityEventStatus.ENDED)

    async def copy_activity_visits(self, from_activity_id: int, to_activity_id: int):
        pass