import telebot

# BotFather bergan API tokenni ' ' belgilari orasiga qo'ying
TOKEN = '8790640164:AAF4l-SBZIY9sVB1BgtgE2KtKils3IRmOGA'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    # Tugmalarni yaratish
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("⚖️ Aliment tartibi")
    btn2 = telebot.types.KeyboardButton("🏠 Uy-joy nizolari")
    btn3 = telebot.types.KeyboardButton("📞 Savol yo'llash")
    
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(message.chat.id, 
                     "Assalomu alaykum! Yuridik yordam botiga xush kelibsiz.\nKerakli bo'limni tanlang:", 
                     reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "⚖️ Aliment tartibi":
        text = ("Aliment undirish uchun kerakli hujjatlar:\n"
                "1. Da'vo ariza\n"
                "2. Bolaning tug'ilganlik guvohnomasi nusxasi\n"
                "3. Nikoh guvohnomasi (yoki bekor qilinganlik haqida guvohnoma)")
        bot.send_message(message.chat.id, text)
        
    elif message.text == "🏠 Uy-joy nizolari":
        bot.send_message(message.chat.id, "Uy-joy masalalari bo'yicha nizolarni sud tartibida hal qilish uchun kadastr hujjatlarini tayyorlang.")
        
    elif message.text == "📞 Savol yo'llash":
        bot.send_message(message.chat.id, "Marhamat, savolingizni yozib qoldiring. Mutaxassislarimiz tez orada sizga javob berishadi.")
    
    else:
        bot.send_message(message.chat.id, "Tushunmadim, iltimos menyudagi tugmalardan foydalaning.")

# Botni ishga tushirish
if name == "main":
    print("Bot ishga tushdi...")
    bot.polling(none_stop=True)
