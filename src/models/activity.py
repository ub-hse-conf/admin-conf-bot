import enum
from dataclasses import dataclass
from datetime import timedelta


class ActivityType(enum.Enum):
    LECTURE = "TED-лекция"
    CONTEST = "Конкурс проектов"
    WORKSHOP = "Мастер-класс"


@dataclass
class Activity:
    id: int
    name: str
    description: str
    activity_type: ActivityType
    has_event: bool
    location: str
    start_time: str
    end_time: str


class ActivityEventStatus(enum.Enum):
    PREPARED = 1
    CONTINUED = 2
    ENDED = 3


@dataclass
class ActivityEvent:
    name: str
    duration: timedelta | None
    status: ActivityEventStatus
