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
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def yts(bot, update):
    search()
def main():
    updater = Updater("1250079555:AAGxMQFXbCTR7hQCFcc7uLXzCYMyvEiTCU8")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('yts',yts))
    dp.add_handler(CommandHandler('1337x',1337x))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()