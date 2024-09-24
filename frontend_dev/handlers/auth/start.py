import json
import requests

from telebot.types import Message

from frontend_dev.loader import bot
from frontend_dev.states.states_bot import States
from frontend_dev.config_info.config import BACK_URL
from frontend_dev.handlers.request_methods import check_user_db, register_check_request


@bot.message_handler(commands=["start"])
def bot_start(m: Message):
    """Запуск бота и приветствие"""

    result = check_user_db(telegram_id=m.from_user.id)

    if result.status_code == 401:
        bot.send_message(
            m.chat.id,
            "You are not registered, please enter your password(Remember it, the message will be deleted:",
        )
        bot.set_state(m.from_user.id, States.set_pass, m.chat.id)

    elif result.status_code == 200:
        bot.reply_to(
            m,
            f"Hello, {m.from_user.full_name}. Use the bot's commands /help",
        )

    else:
        bot.reply_to(
            m,
            f"Bot error, repeat the request /start",
        )


@bot.message_handler(state=States.set_pass)
def registration(m: Message):
    message_pass = m.text

    if message_pass:
        bot.delete_message(chat_id=m.chat.id, message_id=m.message_id)
        if len(message_pass) > 8:
            with bot.retrieve_data(m.from_user.id, m.chat.id) as data:
                data["message_pass"] = message_pass

            data = {
                "username": m.from_user.full_name,
                "telegram_id": m.from_user.id,
                "password": data["message_pass"],
                "is_active": True,
            }

            check_user = register_check_request(data=data)

            if check_user.status_code == 200:
                bot.send_message(
                    m.chat.id,
                    f"You have successfully registered! {m.from_user.full_name}."
                    f"Use the bot's commands /help",
                )
        else:
            bot.send_message(
                m.chat.id,
                "The password is weak, it should be more than 8 characters. Write the password again.",
            )
