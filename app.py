"""Telegram bot to get torrent based on the user's query from yts and 1337x."""

import torrent
from movies import movies
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram import ParseMode
from os import environ
from dotenv import load_dotenv
import re

obj = movies()
load_dotenv()
TOKEN = environ.get("TOKEN")
SONG = environ.get("SONG")


def start(update, context):
    """Send instructions."""
    chat_id = update.message.chat.id
    message = "You can download torrent and srt files from "
    message += "*1337x*, *yts* and *yts-subs*.\n\n"
    message += "Use the following commands to do so.\n\n"
    message += "/1337x - to search from *1337x*.\n\n"
    message += "/yts - to search from *yts*.\n\n"
    message += "/subs - to search from *yts-subs*.\n\n"
    message += "For eg. /yts Rango"
    update.message.reply_text("Hi, I'm Rango.", parse_mode=ParseMode.MARKDOWN)
    context.bot.send_audio(chat_id=chat_id, audio=SONG)
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


def subs(update, context):
    """Search for subs."""
    message = update.message.text
    message = re.findall("/subs (.*)", message)
    message = torrent.search_subs(message[0], obj)
    update.message.reply_text(message)


def yts(update, context):
    """Search for torrent from yts and send the results to the user."""
    message = update.message.text
    message = re.findall("/yts (.*)", message)
    message = torrent.search(message[0], obj)
    update.message.reply_text(message)


def x(update, context):
    """Search for torrent from 1337x and send the results to the user."""
    message = update.message.text
    message = re.findall("/1337x (.*)", message)
    message = torrent.search_1337x(message[0], obj)
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


def reply(update, context):
    """Send the torrent file based the selected search result."""
    query = update.message.text

    try:
        href, message = torrent.quality(int(query), obj)
        try:
            href, message = torrent.get_subs(int(query), obj)
        except Exception as e:
            print(e)
        # If the function quality returns an empty list then
        # get_magnet_1337x() is called
        if href == []:
            href = torrent.get_magnet_1337x(int(query), obj)
        # If the function returns an empty list it means no link is found.
        if href == []:
            text = "Download link not found."
        else:
            text = "You can download the torrent from the following links\n\n"
            i = 0
            for link in href:
                if message != "":
                    # Inline url is created for yts torrent links an not for
                    # 1337x since 1337x returns magnet links
                    # which cannot be used as an inline url in telegram.
                    text += "[{}]({})\n".format(message[i], link)
                else:
                    text += "{}.{}\n\n".format(i + 1, link)
                i += 1
    except Exception as e:
        print(e)
        text = "Enter a valid query\n\nFor eg. /yts Joker"

    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


def main():
    """Initiate bot."""
    updater = Updater(TOKEN, use_context=True)  # Enter your token here
    dp = updater.dispatcher
    # Handlers are created for getting torrent from specified websites.
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('yts', yts))
    dp.add_handler(CommandHandler('1337x', x))
    dp.add_handler(CommandHandler('subs', subs))
    dp.add_handler(MessageHandler(Filters.text, reply))
    # By default timeout is 0.
    updater.start_polling(timeout=180)
    updater.idle()


if __name__ == '__main__':
    main()
