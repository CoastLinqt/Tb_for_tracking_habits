from telebot.types import Message
from frontend_dev.loader import bot

@bot.message_handler(commands=["help"])
def bot_help(m: Message):

    text = "/help — помощь по командам бота.\n" \
           "/"
    bot.send_message(m.chat.id, text, parse_mode='html')