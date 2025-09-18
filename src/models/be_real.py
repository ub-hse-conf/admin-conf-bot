import enum
from dataclasses import dataclass
from datetime import timedelta


class BeRealStatus(enum.Enum):
    READY = 1
    IN_PROCESS = 2
    FINISHED = 3


@dataclass
class BeReal:
    id: int
    name: str
    description: str
    status: BeRealStatus
    duration: timedelta