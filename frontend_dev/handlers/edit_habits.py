from telebot.types import Message, CallbackQuery

from loader import bot
from requests_methods.request_methods import (
    check_user_db,
    edit_habit_request,
    delete_habit_request,
    habits_all,
)
from states.states_bot import States
from keyboards.keyboards_answr import (
    pick_edit,
    delete_or_edit_habit,
    choice_edit_habit,
)


@bot.message_handler(
    commands=["edit_habit"],
)
def edit_habit(message: Message):
    """The handler requests to delete or edit the habit.
    The data is sent to the server and entered into the database
     and the 200 status is returned """

    dict_id = {"telegram_id": message.from_user.id}

    result = check_user_db(telegram_id=message.from_user.id)

    if result.status_code == 401:
        bot.send_message(
            message.chat.id,
            "You're not registered, /start",
        )

    elif result.status_code == 200:
        response = habits_all(data=dict_id)

        result_response = response.json()

        if not result_response:
            bot.reply_to(message, f"You haven't had habits yet. Add /add_habit")
        else:
            result = pick_edit(data=result_response)

            bot.send_message(
                message.from_user.id,
                f"{message.from_user.full_name}, Your habits, choose.",
                reply_markup=result,
            )
            bot.set_state(message.from_user.id, States.save_habit_name, message.chat.id)

    else:
        bot.reply_to(
            message,
            f"Error bot, repeat request /edit_habit",
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
            f"Choose: {name_habit[1:]}",
            reply_markup=buttons_choice,
        )


@bot.callback_query_handler(func=lambda call: call.data == "Edit")
def callback_edit_habit(call: CallbackQuery):
    if call.data:
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )

        result = choice_edit_habit()

        bot.send_message(call.from_user.id, f"Let's start editing", reply_markup=result)


@bot.callback_query_handler(
    func=lambda call: call.data == "Delete",
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
            call.from_user.id,
            f'Habit "{data["name_habit"].capitalize()}" was deleted.',
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
            mes = bot.send_message(
                call.from_user.id,
                f"Enter a new goal for the habit {data['name_habit']}:",
            )
            bot.register_next_step_handler(message=mes, callback=next_pick_goal_habit)


def next_pick_goal_habit(message):
    new_habit_goal = message.text
    length = len(new_habit_goal)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["habit_goal"] = new_habit_goal
        data["telegram_id"] = message.from_user.id

    if length < 20:
        edit_habit_request(data=data)

        bot.send_message(message.from_user.id, f"Completed!")

        data.clear()

    else:
        bot.reply_to(
            message,
            f"The total number of characters and letters must not exceed 20."
            f" You've {length}.Repeat request /edit_habit",
        )


@bot.callback_query_handler(func=lambda call: call.data == "description")
def pick_description(call: CallbackQuery):
    if call.data:
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            mes = bot.send_message(
                call.from_user.id,
                f"Enter a new description for the habit {data['name_habit']}:",
            )

            bot.register_next_step_handler(
                message=mes, callback=next_pick_description_habit
            )


def next_pick_description_habit(message: Message):
    new_description = message.text
    length = len(new_description)
    if length < 50:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["description"] = new_description
            data["telegram_id"] = message.from_user.id

        edit_habit_request(data=data)

        bot.send_message(message.from_user.id, f"Completed!")
        data.clear()
    else:
        bot.reply_to(
            message,
            f"The total number of characters and letters must not exceed 50."
            f" You've {length}. Repeat request /edit_habit",
        )


@bot.callback_query_handler(func=lambda call: call.data == "all")
def pick_all(call: CallbackQuery):
    if call.data:
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            mes = bot.send_message(
                call.from_user.id,
                f"Enter a new goal for the habit {data['name_habit']}: ",
            )

            bot.register_next_step_handler(message=mes, callback=next_pick_goal_all)


def next_pick_goal_all(message):
    new_habit_goal = message.text
    length = len(new_habit_goal)
    if length < 20:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["habit_goal"] = new_habit_goal
            data["telegram_id"] = message.from_user.id

        mes = bot.send_message(
            message.chat.id,
            f"Enter a new description for the habit {data['name_habit']}:",
        )

        bot.register_next_step_handler(message=mes, callback=next_pick_description_all)

    else:
        bot.reply_to(
            message,
            f"The total number of characters and letters must not exceed 20."
            f" У вас {length}. Repeat request  /edit_habit",
        )


def next_pick_description_all(message: Message):
    new_description = message.text
    length = len(new_description)
    if length < 50:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["description"] = new_description

        edit_habit_request(data=data)

        bot.send_message(message.from_user.id, f"Completed!")
        data.clear()
    else:
        bot.reply_to(
            message,
            f"The total number of characters and letters must not exceed 50."
            f" You've {length}. Repeat request /edit_habit",
        )
