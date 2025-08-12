import telebot
import requests
from telebot import types
import os

# ربات با توکن از متغیر محیطی
bot = telebot.TeleBot("7698496255:AAHfJ2_-fp_7GmZhtEZLl41s2dsmjjIMw80", parse_mode=None)

# آی‌دی عددی مدیر (شما)
admin_id = 328903570

# قیمت‌های مواد اولیه
raw_material_prices = """
📦 قیمت مواد اولیه امروز:

- پلی‌اتیلن سبک: ۱۸۵,۰۰۰ تومان
- پلی‌پروپیلن: ۱۹۵,۰۰۰ تومان
- پی‌وی‌سی: ۱۵۵,۰۰۰ تومان
- پلی‌استایرن: ۲۱۰,۰۰۰ تومان
"""

# تابع تبدیل عدد به فارسی
def to_persian_number(number):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    number_str = f"{number:,}"
    persian_number = "".join(persian_digits[int(d)] if d.isdigit() else "،" for d in number_str)
    return persian_number

# دکمه شروع اولیه
@bot.message_handler(commands=['start'])
def send_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("شروع")
    markup.add(start_button)
    bot.send_message(message.chat.id, "👋 به ربات نیکان گرانول خوش آمدی!\n\nبرای شروع دکمه زیر رو بزن:", reply_markup=markup)

# نمایش منوی اصلی پس از زدن "شروع"
@bot.message_handler(func=lambda message: message.text == "شروع")
def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("دلار"), types.KeyboardButton("طلا"),
        types.KeyboardButton("قیمت مواد اولیه")
    )
    markup.add(types.KeyboardButton("خرید گرانول"))
    markup.add(
        types.KeyboardButton("شماره تماس"),
        types.KeyboardButton("اینستاگرام"),
        types.KeyboardButton("آدرس سایت")
    )
    bot.send_message(message.chat.id, "✅ منو اصلی:", reply_markup=markup)

# پردازش پیام‌ها
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.text == "دلار" or message.text == "طلا":
        try:
            response = requests.get('https://api.navasan.tech/latest/?api_key=freegSdtaKeXX2f90DTCiKFD8OCUwFom')
            data = response.json()
            if message.text == "دلار":
                bot.reply_to(message, to_persian_number(int(data["usd_sell"]["value"])) + " تومان")
            elif message.text == "طلا":
                bot.reply_to(message, to_persian_number(int(data["18ayar"]["value"])) + " تومان")
        except:
            bot.reply_to(message, "❌ خطا در دریافت قیمت")

    elif message.text == "قیمت مواد اولیه":
        bot.send_message(message.chat.id, raw_material_prices)

    elif message.text == "شماره تماس":
        bot.send_message(message.chat.id, "☎️ شماره تماس: 09123456789")

    elif message.text == "اینستاگرام":
        bot.send_message(message.chat.id, "📸 اینستاگرام:\nhttps://instagram.com/your_page")

    elif message.text == "آدرس سایت":
        bot.send_message(message.chat.id, "🌐 سایت:\nhttps://yourwebsite.com")

    elif message.text == "خرید گرانول":
        bot.send_message(message.chat.id, "✅ درخواست شما ثبت شد. به زودی با شما تماس خواهیم گرفت.")
        bot.send_message(admin_id, f"🛒 سفارش خرید گرانول:\n👤 نام: {message.from_user.first_name}\n📱 آی‌دی: @{message.from_user.username or 'ندارد'}\n🆔 عددی: {message.from_user.id}")

    else:
        bot.reply_to(message, "❗️ لطفا یکی از گزینه‌ها را انتخاب کن.")

# اجرای ربات
bot.infinity_polling()
