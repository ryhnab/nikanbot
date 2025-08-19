# filename: price_bot.py
import telebot
import requests
from telebot import types
import os
from datetime import datetime

# ---------------- تنظیمات ----------------

BOT_TOKEN = "7698496255:AAHfJ2_-fp_7GmZhtEZLl41s2dsmjjIMw80"
ADMIN_ID = 328903570   # آی‌دی عددی ادمین
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

# پیام پیش‌فرض قیمت‌ها
today_prices = "قیمت‌های امروز هنوز ثبت نشده."

# تابع تبدیل عدد به فارسی
def to_persian_number(number):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    number_str = f"{number:,}"
    persian_number = "".join(persian_digits[int(d)] if d.isdigit() else "،" for d in number_str)
    return persian_number

# ---------------- دستورات ربات ----------------

# شروع
@bot.message_handler(commands=['start'])
def send_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("شروع")
    markup.add(start_button)
    bot.send_message(
        message.chat.id,
        "👋 به ربات نیکان گرانول خوش آمدی!\n\nبرای شروع دکمه زیر رو بزن:",
        reply_markup=markup
    )

# نمایش منوی اصلی
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("دلار"), types.KeyboardButton("طلا"), types.KeyboardButton("قیمت مواد اولیه"))
    markup.add(types.KeyboardButton("خرید گرانول"))
    markup.add(types.KeyboardButton("شماره تماس"), types.KeyboardButton("اینستاگرام"), types.KeyboardButton("آدرس سایت"))
    return markup

@bot.message_handler(func=lambda message: message.text == "شروع")
def show_main_menu(message):
    bot.send_message(message.chat.id, "✅ منو اصلی:", reply_markup=main_menu())

# دستور ادمین برای آپدیت قیمت‌ها
@bot.message_handler(commands=['set_prices'])
def set_prices(message):
    global today_prices
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⛔️ شما دسترسی ندارید.")
        return
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "❌ لطفاً متن قیمت‌ها را بعد از دستور بنویسید.")
        return
    
    today_prices = f"📅 قیمت‌های {datetime.now().strftime('%Y-%m-%d')}:\n{args[1]}"
    bot.reply_to(message, "✅ قیمت‌ها آپدیت شد.")

# گرفتن شماره تماس
@bot.message_handler(func=lambda message: message.text == "خرید گرانول")
def request_contact(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    contact_button = types.KeyboardButton("📲 ارسال شماره تماس", request_contact=True)
    markup.add(contact_button)
    bot.send_message(message.chat.id, "لطفا شماره تماس خود را برای ثبت سفارش ارسال کنید:", reply_markup=markup)

# دریافت شماره تماس و ارسال به ادمین
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact is not None:
        phone_number = message.contact.phone_number
        user_name = message.from_user.first_name
        username = message.from_user.username or "ندارد"
        user_id = message.from_user.id

        bot.send_message(message.chat.id, "✅ شماره تماس شما دریافت شد. به زودی با شما تماس خواهیم گرفت.")
        bot.send_message(
            ADMIN_ID,
            f"🛒 سفارش خرید گرانول:\n👤 نام: {user_name}\n📱 آی‌دی: @{username}\n🆔 عددی: {user_id}\n📞 شماره تماس: {phone_number}"
        )

        # بازگشت به منوی اصلی
        bot.send_message(message.chat.id, "🔙 به منوی اصلی برگشتی:", reply_markup=main_menu())

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
        bot.send_message(message.chat.id, today_prices)

    elif message.text == "شماره تماس":
        bot.send_message(message.chat.id, "☎️ شماره تماس: 09121938795")

    elif message.text == "اینستاگرام":
        bot.send_message(message.chat.id, "📸 اینستاگرام:\nhttps://instagram.com/nikangranol")

    elif message.text == "آدرس سایت":
        bot.send_message(message.chat.id, "🌐 سایت:\nhttps://nikangranol.ir")

    else:
        bot.reply_to(message, "❗️ لطفا یکی از گزینه‌ها را انتخاب کن.")

# ---------------- اجرای ربات ----------------
bot.infinity_polling()
