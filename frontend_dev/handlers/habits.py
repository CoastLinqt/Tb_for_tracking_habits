import json
import requests

from telebot.types import Message
from frontend_dev.loader import bot
from frontend_dev.requests_methods.request_methods import check_user_db
from frontend_dev.config_info.config import BACK_URL
from frontend_dev.helping_func.help_func import create_table


@bot.message_handler(commands=["habits"])
def send_table(message: Message):
    """The handler receives data from the database from the server
    and shows it to the client"""

    result = check_user_db(telegram_id=message.from_user.id)

    if result.status_code == 401:
        bot.send_message(
            message.chat.id,
            "You're not registered, /start",
        )

    elif result.status_code == 200:
        result_db = requests.post(
            url=f"{BACK_URL}/user/me/habits/",
            data=json.dumps({"telegram_id": message.from_user.id}),
        )
        info_habits = result_db.json()

        if result_db.status_code == 200:
            table = create_table(data=info_habits)

            bot.send_message(
                chat_id=message.chat.id,
                text=f"Your habits {message.from_user.full_name} ```{table}```",
                parse_mode="Markdown",
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text=f"You haven't had habits yet. Add /add_habit",
            )

    else:
        bot.reply_to(
            message,
            f"Error bot, repeat request /habits",
        )
