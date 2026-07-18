import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# API Anahtarlarını Alıyoruz
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Lütfen TELEGRAM_TOKEN ve GEMINI_API_KEY değişkenlerini tanımlayın!")

# Kurulumlar
bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Flask (Render Canlı Tutma)
app = Flask(__name__)

@app.route('/')
def home():
    return "Gemini Bot Aktif!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Telegram Komutları
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Selam! Gemini destekli asistanın aktif. Sorularını bekliyorum!")

@bot.message_handler(func=lambda message: True)
def chat_with_gemini(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Bir hata oluştu, lütfen tekrar dene.")
        print(f"Hata: {e}")

if __name__ == "__main__":
    server_thread = Thread(target=run_web_server)
    server_thread.start()
    bot.infinity_polling()
