import os
import telebot
import google.generativeai as genai

# Render'daki ayarlardan şifreleri otomatik çeker
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
# En güncel ve hızlı modeli kullanıyoruz
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Selam! Gemini destekli asistanın aktif. Sorularını bekliyorum!")

@bot.message_handler(func=lambda message: True)
def ask_gemini(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Bir hata oluştu. Lütfen tekrar dene.")

bot.polling()
