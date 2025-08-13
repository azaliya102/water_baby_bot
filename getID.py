import telebot
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(token=TOKEN)

updates = bot.get_updates()
for update in updates:
    print(update.message.chat.id)

