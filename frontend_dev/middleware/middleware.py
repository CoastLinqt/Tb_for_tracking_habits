from frontend_dev.loader import bot


def send_message_middleware(my_bot: bot, chat_id: int, name_habit: str):
    my_bot.send_message(
        chat_id, f"We're here. Don't forget about your habit {name_habit}!"
    )
