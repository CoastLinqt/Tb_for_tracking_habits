import json
import requests

from telebot.types import Message

from frontend_dev.loader import bot
from frontend_dev.states.states_bot import States
from frontend_dev.config_info.config import BACK_URL
from .request_methods import check_user_db


@bot.message_handler(commands=["start"])
def bot_start(m: Message):
    """Запуск бота и приветствие"""

    result = check_user_db(telegram_id=m.from_user.id)

    if result.status_code == 401:
        bot.send_message(
            m.chat.id,
            "Вы не зарегистрированы, пожалуйста введите пароль(Запомните его,"
            " сообщение удалится):",
        )

        bot.set_state(m.from_user.id, States.set_pass, m.chat.id)
    elif result.status_code == 200:
        bot.reply_to(
            m,
            f"Здравствуйте, {m.from_user.full_name}. Воспользуйтесь командами бота /help",
        )

    else:

        bot.reply_to(
            m,
            f"Ошибка бота, повторите запрос /start",
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

            check_user_db = requests.post(
                url=f"{BACK_URL}/token/",
                data=json.dumps(data),
            )
            if check_user_db.status_code == 200:
                bot.send_message(
                    m.chat.id,
                    f"Вы успешно зарегистрированы! {m.from_user.full_name}."
                    f" Воспользуйтесь командами бота /help",
                )
        else:

            bot.send_message(
                m.chat.id,
                "Пароль слабоват должно быть больше 8 знаков. Напишите еще раз пароль.",
            )
