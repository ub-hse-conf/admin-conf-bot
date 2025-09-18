import enum
from dataclasses import dataclass


class ActivityType(enum.Enum):
    LECTURE = 0
    CONTEST = 1
    WORKSHOP = 2


@dataclass
class Activity:
    id: int
    name: str
    description: str
    activity_type: ActivityType
    location: str
    start_time: str
    end_time: str
