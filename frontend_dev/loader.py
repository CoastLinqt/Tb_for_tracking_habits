from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from frontend_dev.config_info.config import BOT_TOKEN

storage = StateMemoryStorage()
bot = TeleBot(token=BOT_TOKEN, state_storage=storage)
