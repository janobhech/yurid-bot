import telebot
import os
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. FLASK SERVER
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# 2. KONFIGURATSIYA
TOKEN = os.environ.get('TOKEN')
GEMINI_KEY = os.environ.get('GOOGLE_API_KEY')

if not TOKEN:
    raise ValueError("TOKEN topilmadi!")
if not GEMINI_KEY:
    raise ValueError("GOOGLE_API_KEY topilmadi!")

# Gemini ulash
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Bot
bot = telebot.TeleBot(TOKEN)

# Har bir foydalanuvchi uchun suhbat tarixi
chat_histories = {}

# 3. /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    chat_histories[user_id] = []
    bot.reply_to(message, 
        "Salom! Men Gemini AI bilan ishlaydigan botman. "
        "Menga istalgan savol bering! 🤖"
    )

# 4. /clear komandasi - suhbatni tozalash
@bot.message_handler(commands=['clear'])
def clear(message):
    user_id = message.chat.id
    chat_histories[user_id] = []
    bot.reply_to(message, "Suhbat tarixi tozalandi! ✅")

# 5. Barcha xabarlar
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user_text = message.text

    # Tarix yo'q bo'lsa yaratish
    if user_id not in chat_histories:
        chat_histories[user_id] = []

    try:
        # "Yozmoqda..." ko'rsatish
        bot.send_chat_action(message.chat.id, 'typing')

        # Suhbat tarixiga qo'shish
        chat_histories[user_id].append({
            "role": "user",
            "parts": [user_text]
        })

        # Gemini'ga yuborish
        chat = model.start_chat(history=chat_histories[user_id][:-1])
        response = chat.send_message(user_text)
        bot_reply = response.text

        # Javobni tarixga qo'shish
        chat_histories[user_id].append({
            "role": "model",
            "parts": [bot_reply]
        })

        # Javob yuborish
        bot.reply_to(message, bot_reply)

    except Exception as e:
        print(f"Xato: {e}")
        bot.reply_to(message, "Xatolik yuz berdi, qayta urinib ko'ring! ⚠️")

# 6. ISHGA TUSHIRISH
if__name__=="__main__":
    keep_alive()
    print("Bot ishga tushdi...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
