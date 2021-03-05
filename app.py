"""Telegram bot to get torrent based on the user's query from yts and 1337x."""

import torrent
from movies import movies
from books import search_books, download_books
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
    message = "You can download books, torrent and srt files from "
    message += "*1337x*, *yts* and *yts-subs*.\n\n"
    message += "Use the following commands to do so.\n\n"
    message += "/1337x - to search from *1337x*.\n\n"
    message += "/yts - to search from *yts*.\n\n"
    message += "/subs - to search from *yts-subs*.\n\n"
    message += "/books - to search for books.\n\n"
    message += "For eg. /yts Rango"
    update.message.reply_text("Hi, I'm Rango.", parse_mode=ParseMode.MARKDOWN)
    context.bot.send_audio(chat_id=chat_id, audio=SONG)
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


def subs(update, context):
    """Search for subs."""
    chatid = update.message.chat.id
    message = update.message.text
    obj.chatid(chatid)
    message = re.findall("/subs (.*)", message)
    message = torrent.search_subs(message[0], chatid, obj)
    obj.command(chatid, "subs")
    update.message.reply_text(message)


def yts(update, context):
    """Search for torrent from yts and send the results to the user."""
    chatid = update.message.chat.id
    obj.chatid(chatid)
    message = update.message.text
    message = re.findall("/yts (.*)", message)
    message = torrent.search(message[0], chatid, obj)
    obj.command(chatid, "yts")
    update.message.reply_text(message)


def x(update, context):
    """Search for torrent from 1337x and send the results to the user."""
    chatid = update.message.chat.id
    message = update.message.text
    obj.chatid(chatid)
    message = re.findall("/1337x (.*)", message)
    message = torrent.search_1337x(message[0], chatid, obj)
    obj.command(chatid, "1337x")
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


def books(update, context):
    """Search for books."""
    chatid = update.message.chat.id
    message = update.message.text
    obj.chatid(chatid)
    message = re.findall("/books (.*)", message)
    message = search_books(chatid, message[0], obj)
    obj.command(chatid, "books")
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


def reply(update, context):
    """Send the torrent file based the selected search result."""
    query = update.message.text
    chatid = update.message.chat.id
    message = ""
    command = obj.get_command(chatid)
    try:
        if command == "yts":
            href, message = torrent.quality(int(query), chatid, obj)
        elif command == "subs":
            href, message = torrent.get_subs(int(query), chatid, obj)
        elif command == "books":
            href, message = download_books(chatid, int(query), obj)
        # If the function quality returns an empty list then
        # get_magnet_1337x() is called
        else:
            href = torrent.get_magnet_1337x(int(query), chatid, obj)
        # If the function returns an empty list it means no link is found.
        if href == []:
            text = "Download link not found."
        else:
            text = ""
            if command != "1337x":
                text = "You can download from the following links\n\n"
                for i, link in enumerate(href):
                    # Inline url is created for yts torrent links an not for
                    # 1337x since 1337x returns magnet links
                    # which cannot be used as an inline url in telegram.
                    text += "[{}]({})\n".format(message[i], link)
            else:
                text = "Paste any of the following magnetic link in your"
                text += " torrent client.\n\n"
                for i, link in enumerate(href):
                    text += "{}. {}\n\n".format(i + 1, link)
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
    dp.add_handler(CommandHandler('books', books))
    dp.add_handler(MessageHandler(Filters.text, reply))
    # By default timeout is 0.
    updater.start_polling(timeout=180)
    updater.idle()


if __name__ == '__main__':
    main()
