import json
import requests

from telebot.types import Message
from frontend_dev.loader import bot
from .request_methods import check_user_db
from frontend_dev.config_info.config import BACK_URL
from .help_func import create_table

@bot.message_handler(commands=["habits"])
def send_table(message: Message):

    result = check_user_db(telegram_id=message.from_user.id)

    if result.status_code == 401:
        bot.send_message(
            message.chat.id,
            "Вы не зарегистрированы, /start",
        )

    elif result.status_code == 200:
        result_db = requests.post(
            url=f"{BACK_URL}/user/me/habits/",
            data=json.dumps({"telegram_id": message.from_user.id}),
        )
        info_habits = result_db.json()
        if info_habits:
            table = create_table(data=info_habits)

            bot.send_message(
                chat_id=message.chat.id,
                text=f"Ваши привычки {message.from_user.full_name} ```{table}```",
                parse_mode="Markdown",
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=f"У вас еще нет привычек. Добавьте /add_habit",
            )

    else:
        bot.reply_to(
            message,
            f"Ошибка бота, повторите запрос /add_habit",
        )
