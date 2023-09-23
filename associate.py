import logging
import datetime
import os
import pytz
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update, ParseMode
import threading

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# hardcore way to config the start time
DATE_FILE = "date.txt"
tz = pytz.timezone('Asia/Taipei')

if os.path.exists(DATE_FILE):
    with open(DATE_FILE, 'r') as f:
        start_date_str = f.read().strip()
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').replace(tzinfo=tz)
else:
    start_date = datetime.datetime(2020, 9, 18, tzinfo=tz) #config your start time here


def start(update: Update, context: CallbackContext):
    text = '嗨😉窩是 @PUT_USERNAME_HERE 和 @PUT_2nd_USERNAME_HERE 的交往紀念日機器人'
    update.message.reply_text(text)


def help_command(update: Update, context: CallbackContext):
    text = '🏠可用指令：\n/start 開始使用\n/help 叫出你在看的這個東西\n/time 看看下一次紀念日是什麼時候\n/setdate 設定紀念日日期\n倉庫：https://github.com/Borschts/mytimebot'
    update.message.reply_text(text)

# config start time via command
def set_date(update: Update, context: CallbackContext):
    if context.args:
        try:
            new_date = datetime.datetime.strptime(context.args[0], '%Y-%m-%d').replace(tzinfo=tz)
            global start_date
            start_date = new_date
            with open(DATE_FILE, 'w') as f:
                f.write(new_date.strftime('%Y-%m-%d'))
            update.message.reply_text(f'Successfully set the new date to {new_date.strftime("%Y-%m-%d")}')
        except ValueError:
            update.message.reply_text('Invalid date format. Please use YYYY-MM-DD.')
    else:
        update.message.reply_text('Please provide a date in the format YYYY-MM-DD.')


def get_diff(update: Update, context: CallbackContext):
    today = datetime.datetime.now(tz)
    days_together = (today - start_date).days
    anniversary_date = start_date.replace(year=today.year)
    
    if today >= anniversary_date:
        anniversary_date = anniversary_date.replace(year=today.year + 1)
    
    days_until_anniversary = (anniversary_date - today).days
    years_together = anniversary_date.year - start_date.year
    text = f'❤你們已經在一起*{days_together}天*了！\n' \
           f'距離第{years_together}個紀念日還有*{days_until_anniversary}天*。'
    update.message.reply_text(text, parse_mode='Markdown')


def main():
    updater = Updater(token='PUT_YOUR_TOKEN_HERE', use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("time", get_diff))
    dp.add_handler(CommandHandler("setdate", set_date))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
