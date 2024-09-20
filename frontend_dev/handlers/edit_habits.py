from telebot.types import Message, CallbackQuery
from frontend_dev.loader import bot
from .request_methods import check_user_db, edit_habit_request, delete_habit_request, habits_all

from frontend_dev.states.states_bot import States


from frontend_dev.keyboards.keyboards_answr import (
    pick_edit,
    delete_or_edit_habit,
    choice_edit_habit,
)


@bot.message_handler(commands=["edit_habit"])
def edit_habit(message: Message):
    dict_id = {"telegram_id": message.from_user.id}

    result = check_user_db(telegram_id=message.from_user.id)

    if result.status_code == 401:
        bot.send_message(
            message.chat.id,
            "Вы не зарегистрированы, /start",
        )

    elif result.status_code == 200:

        response = habits_all(data=dict_id)

        result_response = response.json()

        if not result_response:
            bot.reply_to(message, f"У вас еще нет привычек. /add_habit")
        else:
            result = pick_edit(data=result_response)

            bot.send_message(
                message.from_user.id,
                f"{message.from_user.full_name}, ваши привычки, выберите.",
                reply_markup=result,
            )
            bot.set_state(message.from_user.id, States.save_habit_name, message.chat.id)

    else:
        bot.reply_to(
            message,
            f"Ошибка бота, повторите запрос /add_habit",
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("+"))
def process_edit_habit(call: CallbackQuery):
    name_habit = call.data

    if name_habit:
        bot.delete_message(call.message.chat.id, call.message.message_id)

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data["name_habit"] = call.data[1:].capitalize()

        buttons_choice = delete_or_edit_habit()

        bot.send_message(
            call.from_user.id,
            f"Выберите: {name_habit[1:]}",
            reply_markup=buttons_choice,
        )
        bot.set_state(call.from_user.id, States.set_delete_habit, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == "Редактировать")
def edit_habit(call: CallbackQuery):
    if call.data:

        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )

        result = choice_edit_habit()

        bot.send_message(
            call.from_user.id, f"Приступаем редактировать", reply_markup=result
        )


@bot.callback_query_handler(
    func=lambda call: call.data == "Удалить", state=States.set_delete_habit
)
def delete_habit(call: CallbackQuery):
    if call.data:
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data["telegram_id"] = int(call.from_user.id)

        delete_habit_request(data=data)

        bot.send_message(
            call.from_user.id, f'Привычка "{data["name_habit"].capitalize()}" была удалена.'
        )

        data.clear()


@bot.callback_query_handler(
    func=lambda call: call.data == "goal",
)
def pick_goal_habit(call: CallbackQuery):
    if call.data:
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            bot.send_message(
                call.from_user.id,
                f"Введите новую цель для привычки {data['name_habit']}:",
            )

            bot.set_state(call.from_user.id, States.set_goal, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == "description")
def pick_description(call: CallbackQuery):

    if call.data:
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            bot.send_message(
                call.from_user.id,
                f"Введите новое описание для привычки {data['name_habit']}:",
            )

            bot.set_state(
                call.from_user.id, States.set_description, call.message.chat.id
            )


@bot.callback_query_handler(func=lambda call: call.data == "all")
def pick_all(call: CallbackQuery):

    if call.data:
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            bot.send_message(
                call.from_user.id,
                f"Введите новую цель для привычки {data['name_habit']}: ",
            )

            bot.set_state(call.from_user.id, States.set_all_goal, call.message.chat.id)


@bot.message_handler(state=States.set_goal)
def next_pick_goal_habit(message):
    new_habit_goal = message.text
    length = len(new_habit_goal)
    if length < 20:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["habit_goal"] = new_habit_goal
            data["telegram_id"] = message.from_user.id

        edit_habit_request(data=data)

        data.clear()

        bot.send_message(message.from_user.id, f"Успешно!")
    else:
        bot.reply_to(
            message,
            f"Количество символов и букв в сумме не должно превышать 20."
            f" У вас {length}",
        )


@bot.message_handler(state=States.set_description)
def next_pick_description_habit(message: Message):
    new_description = message.text
    length = len(new_description)
    if length < 50:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["description"] = new_description
            data["telegram_id"] = message.from_user.id

        edit_habit_request(data=data)
        data.clear()

        bot.send_message(message.from_user.id, f"Успешно!")
    else:
        bot.reply_to(
            message,
            f"Количество символов и букв в сумме не должно превышать 50."
            f" У вас {length}",
        )


@bot.message_handler(state=States.set_all_goal)
def next_pick_goal_all(message):
    new_habit_goal = message.text
    length = len(new_habit_goal)
    if length < 20:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["habit_goal"] = new_habit_goal
            data["telegram_id"] = message.from_user.id

        bot.send_message(
            message.chat.id,
            f"Введите новое описание для привычки {data['name_habit']}:",
        )

        bot.set_state(message.from_user.id, States.set_all_description, message.chat.id)
    else:
        bot.reply_to(
            message,
            f"Количество символов и букв в сумме не должно превышать 20."
            f" У вас {length}",
        )


@bot.message_handler(state=States.set_all_description)
def next_pick_description_all(message: Message):
    new_description = message.text
    length = len(new_description)
    if length < 50:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["description"] = new_description

        edit_habit_request(data=data)
        data.clear()

        bot.send_message(message.from_user.id, f"Успешно!")
    else:
        bot.reply_to(
            message,
            f"Количество символов и букв в сумме не должно превышать 50."
            f" У вас {length}",
        )
