import telebot
import threading
import time
from datetime import datetime, date
import os
from dotenv import load_dotenv
import random
from telebot import types

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
IMAGES = [
    os.getenv("FIRST_PIC"),
    os.getenv("SECOND_PIC"),
    os.getenv("THIRD_PIC")
]
bot = telebot.TeleBot(TOKEN)

REMINDER_TIMES = [(11, 0), (15, 0), (20, 0)]
sent_today = set()

def send_photo():
    image = random.choice(IMAGES)
    with open(image, 'rb') as img:
        bot.send_photo(chat_id=CHAT_ID, photo=img, caption="🐦 Stay hydrated love! 💧")

def reminder_loop():
    while True:
        now = datetime.now()
        hm = (now.hour, now.minute)
        key = (hm[0], hm[1], date.today())

        if hm in REMINDER_TIMES and key not in sent_today:
            send_photo()
            sent_today.add(key)

        time.sleep(20)

threading.Thread(target=reminder_loop, daemon=True).start()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    calc_btn = types.KeyboardButton("💧 Water Calculator")
    markup.add(calc_btn)

    bot.send_message(
        message.chat.id,
        "Hi! This is your water reminder!💧",
        reply_markup=markup
    )

user_states = {}
@bot.message_handler(content_types=['text'])
def handle_water_request(message):
    chat_id = message.chat.id
    if message.text == "💧 Water Calculator":
        bot.send_message(
            message.chat.id,
            "Please send your height and weight in two numbers separated by a space!"
        )
        user_states[chat_id] = "waiting_for_data"
    elif user_states.get(chat_id) == "waiting_for_data":
        parts = message.text.split()
        if len(parts) == 2:
            try:
                height = int(parts[0])
                weight = int(parts[1])
                bsa = ((height * weight) / 3600) ** 0.5
                water_need = int(bsa * 1200)
                bot.send_message(chat_id, f"you should drink {water_need}ml a day!")
                user_states.pop(chat_id)
            except ValueError:
                bot.send_message(chat_id, "Please enter valid numbers like: 170 65")
        else:
            bot.send_message(chat_id, "Please send exactly two numbers separated by a space.")

bot.polling(none_stop=True)

