import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.environ.get("TOKEN_BOT")
BACK_URL = os.environ.get("BACK_URL")


DEFAULT_COMMANDS = (
    ("start", "User registration"),
    ("help", "Output information"),
)
