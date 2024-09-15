import requests
import telebot

bot = telebot.TeleBot("6944166033:AAHHKSdppLIMBrQWXHnaKoyLhyWsLaMoBc0")


r = requests.get(f'https://api.telegram.org/bot6944166033:AAHHKSdppLIMBrQWXHnaKoyLhyWsLaMoBc0/setWebhook?url=https://2e816886b8d1b4.lhr.life/')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")


bot.infinity_polling()