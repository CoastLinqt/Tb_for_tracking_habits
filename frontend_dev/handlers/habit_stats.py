import json

import requests
from telebot.types import Message
from frontend_dev.loader import bot
from frontend_dev.config_info.config import BACK_URL
from .help_func import track_stats
from .request_methods import check_user_db


@bot.message_handler(
    commands=["habit_stats"],
)
def habit_stats(message: Message):
    data_id = {"telegram_id": message.from_user.id}

    result = check_user_db(telegram_id=message.from_user.id)

    if result.status_code == 401:
        bot.send_message(
            message.chat.id,
            "You're not registered, /start",
        )

    elif result.status_code == 200:
        response = requests.post(
            url=f"{BACK_URL}/habit/habit_stats/", data=json.dumps(data_id)
        )

        result_response = response.json()
        if result_response:
            table = track_stats(result_response)

            bot.send_message(
                chat_id=message.chat.id,
                text=f"Статистика {message.from_user.full_name} ```{table}```",
                parse_mode="Markdown",
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=f"You haven't had habits yet.Add Добавьте /add_habit",
            )

    else:
        bot.reply_to(
            message,
            f"Error bot, repeat request /habit_stats",
        )
