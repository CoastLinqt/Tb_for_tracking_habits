from telebot.types import Message
from frontend_dev.loader import bot


@bot.message_handler(commands=["help"])
def bot_help(m: Message):
    """The handler helps user's with choose commands"""
    text = (
        "/help — help with bot commands.\n"
        "/start — user registration.\n"
        "/add_habit — information about a new habit.\n"
        "/habits — getting a list of habits.\n"
        "/edit_habit — choose a habit to edit.\n"
        "/track_habit — selects a habit to mark the completion.\n"
        "/habit_stats — statistics of habit fulfillment.\n"
        "/set_reminder — a reminder to mark the fulfillment of habits.\n"
    )
    bot.send_message(m.chat.id, text, parse_mode="html")
