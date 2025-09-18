import enum
from dataclasses import dataclass


class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    VOLUNTEER = "volunteer"


@dataclass
class User:
    id: int
    tg_id: int
    role: UserRole
    name: str