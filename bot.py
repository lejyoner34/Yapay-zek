import os
import telebot
from google import genai

# Render ortam değişkenlerinden şifreleri çekiyoruz
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# En güncel v1 API istemcisini başlatıyoruz
client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Selam! Gemini 1.5-Flash destekli asistanın aktif. Sorularını bekliyorum!")

@bot.message_handler(func=lambda message: True)
def ask_gemini(message):
    try:
        # En güncel model çağırma standardı
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=message.text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu. Hata detayı:\n{str(e)}")

bot.infinity_polling()
