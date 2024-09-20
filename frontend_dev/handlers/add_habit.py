# import datetime

from telebot.types import Message
# from telegram_bot_calendar import DetailedTelegramCalendar
#
# from dateutil.relativedelta import relativedelta

from frontend_dev.loader import bot
from frontend_dev.states.states_bot import States
from .request_methods import check_user_db, add_habit_db


# LSTEP: dict[str, str] = {"y": "год", "m": "месяц", "d": "день"}


@bot.message_handler(commands=["add_habit"])
def add_habit(message: Message):
    result = check_user_db(telegram_id=message.from_user.id)

    if result.status_code == 401:
        bot.send_message(
            message.chat.id,
            "Вы не зарегистрированы, /start",
        )

    elif result.status_code == 200:
        bot.send_message(message.chat.id, "Введите название новой привычки:")
        bot.set_state(message.from_user.id, States.add_habit, message.chat.id)

    else:
        bot.reply_to(
            message,
            f"Ошибка бота, повторите запрос /add_habit",
        )


@bot.message_handler(state=States.add_habit)
def add_habit(message: Message):
    message_habit = message.text

    if len(message_habit) < 20:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["add_habit"] = message_habit.capitalize()

        bot.send_message(message.chat.id, "Введите описание новой привычки:")
        bot.set_state(message.from_user.id, States.habit_description, message.chat.id)
    else:
        bot.reply_to(message, f"Количество символов и букв в сумме не должно превышать 20. У вас {len(message_habit)}")


@bot.message_handler(state=States.habit_description)
def process_habit_description(message: Message):
    habit_description = message.text

    if len(habit_description) < 50:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["habit_description"] = habit_description
            data["telegram_id"] = int(message.from_user.id)

        bot.send_message(message.chat.id, "Введите цель  новой привычки:")
        bot.set_state(message.from_user.id, States.habit_goal, message.chat.id)
    else:
        bot.reply_to(message, f"Количество символов и букв в сумме не должно превышать 50."
                              f" У вас {len(habit_description)}")


@bot.message_handler(state=States.habit_goal)
def process_habit_goal(message: Message):
    message_habit_goal = message.text

    if len(message_habit_goal) < 20:

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["message_habit_goal"] = message_habit_goal

        if add_habit_db(data=data):

            bot.send_message(
                message.chat.id, "Новая привычка успешно добавлена!Проверьте /habits"
            )
        else:
            bot.send_message(
                message.chat.id, "Такая привычка уже есть !Проверьте /habits"
            )

    else:
        bot.reply_to(message, f"Количество символов и букв в сумме не должно превышать 20."
                              f" У вас {len(message_habit_goal)}")

# @bot.message_handler(state=States.habit_goal)
# def process_habit_description(message: Message):
#     message_habit_goal = message.text
#
#     if message_habit_goal.isdigit():
#
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data["message_habit_goal"] = int(message_habit_goal)
#             data["telegram_id"] = int(message.from_user.id)
#
#         bot.send_message(
#             message.from_user.id, f"Теперь необходимо выбрать срок выполнения привычки."
#         )
#         calendar_first, step = DetailedTelegramCalendar(
#             calendar_id=1,
#             locale="ru",
#             min_date=datetime.date.today(),
#             max_date=datetime.date.today() + relativedelta(months=2),
#         ).build()
#         #
#
#         bot.send_message(
#             message.chat.id, f"Выберите {LSTEP[step]}", reply_markup=calendar_first
#         )
#
#         bot.set_state(message.from_user.id, States.habit_date, message.chat.id)
#
#     else:
#         bot.reply_to(message, f"Цель должна быть число.")
#
#
# @bot.callback_query_handler(
#     func=DetailedTelegramCalendar.func(calendar_id=1), state=States.habit_date
# )
# def process_habit_date(
#     call: CallbackQuery,
# ):
#
#     result, key, step = DetailedTelegramCalendar(
#         calendar_id=1, locale="ru", min_date=datetime.date.today()
#     ).process(call.data)
#     if not result and key:
#         bot.edit_message_text(
#             f"Выберите {LSTEP[step]}",
#             call.message.chat.id,
#             call.message.message_id,
#             reply_markup=key,
#         )
#
#     elif result:
#         date_format = "%d-%m-%Y"
#
#         bot.delete_message(
#             chat_id=call.message.chat.id, message_id=call.message.message_id
#         )
#         with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
#             data["habit_date"] = result.strftime(date_format)
#
#         add_habit_db(data=data)
#
#         bot.send_message(
#             call.message.chat.id, "Новая привычка успешно добавлена!Проверьте /habits"
#         )
