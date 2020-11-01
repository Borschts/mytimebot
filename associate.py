import logging
import datetime
import time
import json
import requests
import _thread
import urllib3
from telegram.ext import Updater, CommandHandler, MessageHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.INFO)

logger = logging.getLogger(__name__)
cnt = 0

def start(update, context):
global cnt; cnt += 1; print(cnt)
text = '嗨😉\n窩是 @Morishima_Hodaka_TG 和 @Shawn_N 的交往紀念日機器人'
msg = update.message.reply_text(text)
try:
_thread.start_new_thread(delete_message_thread, (update, context, msg, text))
except:
print ("Error: unable to start thread.")


def help_command(update, context):
global cnt; cnt += 1; print(cnt)
text = '🏠可用指令：\n/start 開始使用\n/help 叫出你在看的這個東西\n/time 看看下一次紀念日是什麼時候'
msg = update.message.reply_text(text)
try:
_thread.start_new_thread(delete_message_thread, (update, context, msg, text))
except:
print ("Error: unable to start thread.")

def delete_message_thread(update, context, msg, text):
cnt = 30
while(cnt > 0):
time.sleep(6)
try:
msg.edit_text(text= text + '\n⏰避免為群組帶來干擾，本訊息將於'+str(cnt-6)+'秒後自動刪除。', parse_mode='Markdown')
cnt -= 6
except Exception as e:
print("Message {} got exception {}".format(msg, e))
time.sleep(2)
context.bot.deleteMessage(chat_id=msg.chat.id, message_id=msg.message_id) 

def getDiff(update, context):
global cnt; cnt += 1; print(cnt)
today = datetime.datetime.today()
associate_day = datetime.datetime(today.year, 09, 18)
diff = (associate_day - today).days
year = today.year + 1
if diff < 0:
next_associate_day = datetime.datetime(today.year + 1, 09, 18)
diff = (next_associate_day - today).days
year += 1
text = '❤距離' + str(year) + '下次紀念日還有*' + str(diff) + ' *天.'
msg = update.message.reply_text(text, parse_mode='Markdown')

def main():
updater = Updater(token='TOKEN', use_context=True, request_kwargs={'read_timeout': 30, 'connect_timeout': 30})
# 註冊handler
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help_command))
dp.add_handler(CommandHandler("time", getDiff))

updater.start_polling()
updater.idle()


if name == '__main__':
main()
