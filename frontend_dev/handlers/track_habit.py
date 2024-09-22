import json

import requests
from telebot.types import Message, CallbackQuery
from frontend_dev.loader import bot
from frontend_dev.config_info.config import BACK_URL
from frontend_dev.handlers.request_methods import check_user_db, edit_habit_request, delete_habit_request, habits_all
from frontend_dev.states.states_bot import States
from frontend_dev.keyboards.keyboards_answr import (
    pick_track,
    delete_or_edit_habit,
    choice_edit_habit,
)

dict_new = [{"name_habit": "Test", "habit_goal": "habit_goal", "description": "description"},
            {"name_habit": "Ok", "habit_goal": "habit_goal", "description": "description"},
            {"name_habit": "next", "habit_goal": "habit_goal", "description": "description"},
            {"name_habit": "right", "habit_goal": "habit_goal", "description": "description"},
            {"name_habit": "left", "habit_goal": "habit_goal", "description": "description"}]


@bot.message_handler(commands=["track_habit"],)
def track_habit(message):
    dict_id = {"telegram_id": message.from_user.id}

    response = requests.post(url=f'{BACK_URL}/habit/track_all/', data=json.dumps(dict_id))

    result_response = response.json()
    if result_response:

        reply = pick_track(data=result_response)

        bot.send_message(message.chat.id, 'Выберите привычку, которую выполнили ', reply_markup=reply)
    else:
        bot.send_message(message.chat.id, 'Вы выполнили все привычки!')


@bot.callback_query_handler(func=lambda call: call.data.startswith("*"))
def process_track_habit(call: CallbackQuery):
    habit_name = call.data[1:]
    if habit_name:
        data_my = {"telegram_id": call.from_user.id, "name_habit": habit_name}

        result = requests.post(url=f'{BACK_URL}/habit/edit/track/', data=json.dumps(data_my))
        print()
        if result.status_code == 200:
            bot.send_message(call.from_user.id, f'Молодец!Ты выполнили привычку {habit_name}')

        elif result.status_code == 500:
            bot.send_message(call.from_user.id, 'Ты полностью выполнил привычку, поздравляю!!')


