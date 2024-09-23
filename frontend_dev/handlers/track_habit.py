import json

import requests
from telebot.types import CallbackQuery

from frontend_dev.loader import bot
from frontend_dev.config_info.config import BACK_URL
from frontend_dev.handlers.request_methods import (
    check_user_db,
)

from frontend_dev.keyboards.keyboards_answr import (
    pick_track,
)
from .request_methods import habit_track_request


@bot.message_handler(
    commands=["track_habit"],
)
def track_habit(message):
    dict_id = {"telegram_id": message.from_user.id}

    result = check_user_db(telegram_id=message.from_user.id)

    if result.status_code == 401:
        bot.send_message(
            message.chat.id,
            "Вы не зарегистрированы, /start",
        )

    elif result.status_code == 200:

        response = habit_track_request(data=dict_id)

        result_response = response.json()
        if result_response:
            reply = pick_track(data=result_response)

            bot.send_message(
                message.chat.id,
                "Выберите привычку, которую выполнили ",
                reply_markup=reply,
            )
        else:
            bot.send_message(message.chat.id, "Вы выполнили все привычки!")

    else:
        bot.reply_to(
            message,
            f"Ошибка бота, повторите запрос /add_habit",
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("*"))
def process_track_habit(call: CallbackQuery):
    habit_name = call.data[1:]
    if habit_name:
        data_my = {"telegram_id": call.from_user.id, "name_habit": habit_name}

        result = requests.post(
            url=f"{BACK_URL}/habit/count_track/", data=json.dumps(data_my)
        )

        if result.status_code == 200:
            bot.send_message(
                call.from_user.id, f"Молодец!Ты выполнили привычку {habit_name}"
            )

        elif result.status_code == 500:
            bot.send_message(
                call.from_user.id, "Ты полностью выполнил привычку, поздравляю!!"
            )
