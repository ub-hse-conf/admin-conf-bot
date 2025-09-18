from src.models import Activity, ActivityType


class ActivityService:
    async def get_activities(self) -> list[Activity]:
        return [
            Activity(
                id=1,
                name="Activity 1",
                description="This is the description of Activity 1",
                activity_type=ActivityType.CONTEST,
                location="Location 1",
                start_time="10:10",
                end_time="12:10"
            )
        ]