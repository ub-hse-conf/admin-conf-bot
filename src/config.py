from decouple import config

from src.models import WorkingMode

SERVER_URL = config("BASE_URL")

REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", default="6379")

REDIS_TTL: int = config("REDIS_TTL", cast=int)

USERNAME_API = config("BOT_USERNAME")
PASSWORD_API = config("BOT_PASSWORD")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
IS_PROD: bool = not DEBUG

BOT_TOKEN = config("BOT_TOKEN")

WORKING_MODE = config("WORKING_MODE", cast=WorkingMode)

WEBHOOK_URL = config("WEBHOOK_URL", default=None)
WEBHOOK_PATH = config("WEBHOOK_PATH", default="/")

MINI_APP_URL = config("MINI_APP_URL")
SCANNER_LOGIN_API = config("SCANNER_LOGIN")
SCANNER_PASSWORD_API = config("SCANNER_PASSWORD")
