import os
import telebot
import google.generativeai as genai

# Render ortam değişkenlerinden şifreleri çekiyoruz
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Değişkenlerin boş olup olmadığını kontrol et
if not TELEGRAM_TOKEN:
    print("HATA: TELEGRAM_TOKEN bulunamadı!")
if not GEMINI_API_KEY:
    print("HATA: GEMINI_API_KEY bulunamadı!")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
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
        # Hata detayını doğrudan bota yazdırıyoruz ki sorunu görelim
        bot.reply_to(message, f"Bir hata oluştu. Hata detayı:\n{str(e)}")

# Botu başlat ve çökmesini engelle
bot.infinity_polling()
