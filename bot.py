# filename: price_bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from datetime import datetime

# ====== تنظیمات اولیه ======
BOT_TOKEN = "7698496255:AAHfJ2_-fp_7GmZhtEZLl41s2dsmjjIMw80"  # توکن رباتت
ADMIN_ID = 328903570          # آی‌دی ادمین

# پیام پیش‌فرض قیمت‌ها
today_prices = "قیمت‌های امروز هنوز ثبت نشده."

# ====== دستورات ربات ======

# دستور /start و نمایش دکمه
def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("لیست قیمت امروز", callback_data='show_prices')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("سلام! یکی از گزینه‌ها را انتخاب کنید:", reply_markup=reply_markup)

# دستور ادمین برای آپدیت قیمت‌ها
def set_prices(update: Update, context: CallbackContext):
    global today_prices
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("شما دسترسی ندارید!")
        return

    if not context.args:
        update.message.reply_text("لطفاً متن قیمت‌ها را بعد از دستور وارد کنید.")
        return

    # ثبت پیام جدید با تاریخ روز
    today_prices = f"📅 قیمت‌های {datetime.now().strftime('%Y-%m-%d')}:\n" + " ".join(context.args)
    update.message.reply_text("✅ قیمت‌ها آپدیت شد.")

# پاسخ به دکمه
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'show_prices':
        query.edit_message_text(text=today_prices)

# ====== اجرای ربات ======
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('set_prices', set_prices))
    dp.add_handler(CallbackQueryHandler(button))

    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
