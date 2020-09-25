import json
import requests
import time
from yts import search,quality, get_magnet_1337x, search_1337x
from movies import movies
import urllib
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, ConversationHandler, Filters
from telegram import ParseMode
import requests
import re

obj = movies()

def bop(bot, update):
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id)

def yts(bot, update):
    chat_id = update.message.chat_id
    message = update.message.text
    message = re.findall("/yts (.*)",message)
    message = search(message[0],obj)
    bot.send_message(chat_id=chat_id,text=message)

def x(bot,update):
    chat_id = update.message.chat_id
    message = update.message.text
    message = re.findall("/1337x (.*)",message)
    message = search_1337x(message[0],obj)
    bot.send_message(chat_id=chat_id,text=message)

def reply(bot,update):
    chat_id = update.message.chat_id
    query = update.message.text
    try:
        href,message = quality(int(query),obj)
        if href == []:
            href = get_magnet_1337x(int(query),obj)
        if href == []:
            text = "Download link not found."
        else:
            text = "You can download the torrent from the following links\n\n"
            i = 0
            replacements = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
            for link in href:
                for replacement in replacements:
                    link = link.replace(replacement,'\\{}'.format(replacement))
                    if message != "":
                        message[i] = message[i].replace(replacement,'\\{}'.format(replacement))
                if message != "":
                    text += "[{}]({})\n".format(message[i],link)
                else:
                    text += "{}\\.{}\n\n".format(i+1,link)
                i += 1
    except:
        text = "Enter a valid query\nFor eg\\. /yts \\{query\\} or /1337x \\{query\\}"
        
    bot.send_message(chat_id=chat_id,text=text,parse_mode=ParseMode.MARKDOWN_V2)


def main():
    updater = Updater("1250079555:AAGxMQFXbCTR7hQCFcc7uLXzCYMyvEiTCU8")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('yts',yts))
    dp.add_handler(CommandHandler('1337x',x))
    dp.add_handler(MessageHandler(Filters.text,reply))
    updater.start_polling(timeout=180)
    updater.idle()

if __name__ == '__main__':
    main()