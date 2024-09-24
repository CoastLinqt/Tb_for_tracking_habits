import datetime
from datetime import timedelta
from telebot.types import CallbackQuery, Message
from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.relativedelta import relativedelta

from frontend_dev.loader import bot
from frontend_dev.keyboards.keyboards_answr import (
    set_habit,
)
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from frontend_dev.keyboards.keyboards_answr import pick_time
from frontend_dev.states.states_bot import States
from frontend_dev.requests_methods.request_methods import (
    check_user_db,
    set_reminder_request,
    habit_track_request,
)
from frontend_dev.middleware.middleware import send_message_middleware


@bot.message_handler(
    commands=["set_reminder"],
)
def set_reminder(message: Message):
    """The handler sends specific data to the server, processes it,
     and sends a notification on a given date that you need to perform the habit"""

    dict_id = {"telegram_id": message.from_user.id}

    result = check_user_db(telegram_id=message.from_user.id)

    if result.status_code == 401:
        bot.send_message(
            message.chat.id,
            "You're not registered, /start",
        )

    elif result.status_code == 200:
        response = habit_track_request(data=dict_id)
        result = response.json()
        if response.status_code == 200:
            markup = set_habit(data=result)

            bot.send_message(
                message.from_user.id,
                f"{message.from_user.full_name}, your habits, choose one.",
                reply_markup=markup,
            )

            bot.set_state(message.from_user.id, States.set_reminder, message.chat.id)
        else:
            bot.send_message(
                message.chat.id, "You haven't had a habit yet or you completed! /habits"
            )

    else:
        bot.reply_to(
            message,
            f"Error bot, repeat request /set_reminder",
        )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("-"), state=States.set_reminder
)
def processset_reminder(call: CallbackQuery):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    bot.send_message(
        call.from_user.id,
        f"Now you need to choose a deadline for completing the habit.",
    )

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data["telegram_id"] = int(call.from_user.id)
        data["name_habit"] = call.data[1:]

    calendar_first, step = DetailedTelegramCalendar(
        calendar_id=1,
        locale="ru",
        min_date=datetime.date.today() + timedelta(days=1),
        max_date=datetime.date.today() + relativedelta(months=2),
    ).build()

    bot.send_message(
        call.message.chat.id, f"Choose {LSTEP[step]}", reply_markup=calendar_first
    )


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def process_habit_date(
    call: CallbackQuery,
):
    result, key, step = DetailedTelegramCalendar(
        calendar_id=1, locale="ru", min_date=datetime.date.today()
    ).process(call.data)
    if not result and key:
        bot.edit_message_text(
            f"Choose {LSTEP[step]}",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=key,
        )

    elif result:
        date_format = "%d-%m-%Y"

        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data["habit_date"] = result.strftime(date_format)

        msg = bot.send_message(
            call.from_user.id, "Choose specific time", reply_markup=pick_time()
        )
        bot.register_next_step_handler(message=msg, callback=data_infi_about_user)


def data_infi_about_user(message: Message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["time"] = message.text

    response = set_reminder_request(data=data)
    response_result = response.json()

    if response_result:
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            send_message_middleware,
            "date",
            run_date=response_result["habit_date"],
            kwargs={
                "my_bot": bot,
                "chat_id": message.from_user.id,
                "name_habit": response_result["name_habit"],
            },
        )

        scheduler.start()

        bot.send_message(
            message.from_user.id, "Completed, we've remembered your habit!"
        )
