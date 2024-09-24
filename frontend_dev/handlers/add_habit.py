from telebot.types import Message


from frontend_dev.loader import bot
from frontend_dev.states.states_bot import States
from frontend_dev.requests_methods.request_methods import check_user_db, add_habit_db


@bot.message_handler(commands=["add_habit"])
def add_habit(message: Message):
    """The handler asks several questions,
     the name, description and purpose of the habit,
      and later sends the information to the server.
      The server processes and returns the 200 status """

    result = check_user_db(telegram_id=message.from_user.id)

    if result.status_code == 401:
        bot.send_message(
            message.chat.id,
            "You're not registered, /start",
        )

    elif result.status_code == 200:
        bot.send_message(message.chat.id, "Enter the name of the new habit:")
        bot.set_state(message.from_user.id, States.add_habit, message.chat.id)

    else:
        bot.reply_to(
            message,
            f"Error bot, repeat request /add_habit",
        )


@bot.message_handler(state=States.add_habit)
def process_add_habit(message: Message):
    message_habit = message.text

    if len(message_habit) < 20:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["add_habit"] = message_habit.capitalize()

        bot.send_message(message.chat.id, "Enter a description of the new habit:")
        bot.set_state(message.from_user.id, States.habit_description, message.chat.id)
    else:
        bot.reply_to(
            message,
            f"The total number of characters and letters must not exceed 20. You've {len(message_habit)}",
        )


@bot.message_handler(state=States.habit_description)
def process_habit_description(message: Message):
    habit_description = message.text

    if len(habit_description) < 50:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["habit_description"] = habit_description
            data["telegram_id"] = int(message.from_user.id)

        bot.send_message(message.chat.id, "Enter the purpose of the new habit:")
        bot.set_state(message.from_user.id, States.habit_goal, message.chat.id)
    else:
        bot.reply_to(
            message,
            f"The total number of characters and letters must not exceed  50."
            f" You've {len(habit_description)}",
        )


@bot.message_handler(state=States.habit_goal)
def process_habit_goal(message: Message):
    message_habit_goal = message.text

    if len(message_habit_goal) < 20:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["message_habit_goal"] = message_habit_goal

        if add_habit_db(data=data):
            bot.send_message(
                message.chat.id,
                "A new habit has been successfully added!Check it out /habits",
            )

        else:
            bot.send_message(
                message.chat.id, "This habit already exists!Check it out /habits"
            )
        data.clear()

    else:
        bot.reply_to(
            message,
            f"The total number of characters and letters must not exceed 20."
            f" You've {len(message_habit_goal)}",
        )
