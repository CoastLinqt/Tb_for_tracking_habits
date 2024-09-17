from telebot.types import Message
from frontend_dev.loader import bot


@bot.message_handler(commands=["start"])
def bot_start(m: Message):
    """Запуск бота и приветствие"""

    bot.reply_to(m, f"Здравствуйте, {m.from_user.full_name}")