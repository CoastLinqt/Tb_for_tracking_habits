from telebot.types import Message
from frontend_dev.loader import bot


@bot.message_handler(commands=["help"])
def bot_help(m: Message):
    text = (
        "/help — помощь по командам бота.\n"
        "/start — регистрация пользователя.\n"
        "/add_habit — информация о новой привычке.\n"
        "/habits — получение списка привычек.\n"
        "/edit_habit — выбрать привычку для редактирования.\n"
        "/track_habit — выбирает привычку для отметки выполнения.\n"
        "/habit_stats — статистика выполнения привычек.\n"
        "/set_reminder — напоминание для отметки выполнения привычек.\n"
    )
    bot.send_message(m.chat.id, text, parse_mode="html")
