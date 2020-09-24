import json
import requests
import time
from yts import search,quality
from movies import movies
import urllib
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re

def bop(bot, update):
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id)

def yts(bot, update):
    chat_id = update.message.chat_id
    message = update.message.text
    print(message,chat_id)

def x(bot,update):
    chat_id = update.message.chat_id
    message = update.message.text
    print(message,chat_id)


def main():
    updater = Updater("1250079555:AAGxMQFXbCTR7hQCFcc7uLXzCYMyvEiTCU8")
    dp = updater.dispatcher
    print(dp.chat_data)
    dp.add_handler(CommandHandler('yts',yts))
    dp.add_handler(CommandHandler('1337x',x))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()