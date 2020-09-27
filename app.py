"""A Telegram bot to get torrent based on the user's query from yts and 1337x"""

import json
import requests
import time
from torrent import search, quality, get_magnet_1337x, search_1337x
from movies import movies
import urllib
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, ConversationHandler, Filters
from telegram import ParseMode
import requests
import re
import inspect

obj = movies()

def start(bot, update):

    chat_id = update.message.chat_id
    message = inspect.cleandoc(''' Hi\\! I'm the torrent downloader bot\\.
                You can search from *1337x* or *yts*\\.\n
                Use the following commands to do so\\.\n
                /1337x \\- to search from *1337x*\\.\n
                /yts \\- to search from yts\\.\n
                For eg\\. /yts Inception  '''
                )
    bot.send_message(chat_id = chat_id, text = message, parse_mode = ParseMode.MARKDOWN_V2)

def yts(bot, update):
    """A function to search for torrent from yts and send the results to the user"""

    chat_id = update.message.chat_id
    message = update.message.text
    message = re.findall("/yts (.*)", message)
    message = search(message[0], obj)
    bot.send_message(chat_id = chat_id, text = message)

def x(bot, update):
    """A function to search for torrent from 1337x and send the results to the user"""

    chat_id = update.message.chat_id
    message = update.message.text
    message = re.findall("/1337x (.*)", message)
    message = search_1337x(message[0], obj)
    bot.send_message(chat_id = chat_id, text = message)

def reply(bot, update):
    """A function to send the torrent file based the selected search result"""

    chat_id = update.message.chat_id
    query = update.message.text

    try:
        href,message = quality(int(query),obj)
        # If the function quality returns an empty list then get_magnet_1337x() is called
        if href == []:
            href = get_magnet_1337x(int(query),obj)
        # If the function returns an empty list it means no link is found.
        if href == []:
            text = "Download link not found."
        else:
            text = "You can download the torrent from the following links\n\n"
            i = 0
            # These characters are not accepted in this format in telegram so they have to be modified accordingly.
            replacements = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
            for link in href:
                for replacement in replacements:
                    # If any character from replacements is present then it is replaced with \ before the character.
                    # For eg. * is replaced with \*
                    link = link.replace(replacement, '\\{}'.format(replacement))
                    if message != "":
                        # If message is not empty this means torrent is from yts and the message is modified accoringly.
                        message[i] = message[i].replace(replacement, '\\{}'.format(replacement))
                if message != "":
                    # Inline url is created for yts torrent links an not for 1337x since 1337x returns magnet links
                    # which cannot be used as an inline url in telegram.
                    text += "[{}]({})\n".format(message[i], link)
                else:
                    text += "{}\\.{}\n\n".format(i + 1, link)
                i += 1
    except:
        text = "Enter a valid query\n\nFor eg\\. /yts Joker"
        
    bot.send_message(chat_id = chat_id, text = text, parse_mode = ParseMode.MARKDOWN_V2)


def main():
    updater = Updater("1250079555:AAGxMQFXbCTR7hQCFcc7uLXzCYMyvEiTCU8") # Enter your token here
    dp = updater.dispatcher
    # Handlers are created for getting torrent from specified websites.
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('yts', yts))
    dp.add_handler(CommandHandler('1337x', x))
    dp.add_handler(MessageHandler(Filters.text, reply))
    # By default timeout is 0.
    updater.start_polling(timeout = 180)
    updater.idle()

if __name__ == '__main__':
    main()