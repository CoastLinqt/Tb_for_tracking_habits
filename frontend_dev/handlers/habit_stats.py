import json

import requests
from telebot.types import Message
from loader import bot
from config_info.config import BACK_URL
from helping_func.help_func import track_stats
from requests_methods.request_methods import check_user_db


@bot.message_handler(
    commands=["habit_stats"],
)
def habit_stats(message: Message):
    """The handler receives the client's data and processes it,
     showing the client's statistics """

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
