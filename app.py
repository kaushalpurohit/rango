"""Telegram bot to get torrent based on the user's query from yts and 1337x."""

from __future__ import unicode_literals
import re
from os import environ
from telegram import ParseMode
from dotenv import load_dotenv 
import youtube_dl
from scraper.links import links
from scraper.yts import search_yts, get_quality_yts
from scraper.x import search_1337x, get_magnet_1337x
from scraper.mcqs import generate_pdf
from scraper.games import search_games, get_games
from scraper.subs import search_subs, get_subs
from scraper.lyrics import search_lyrics, get_lyrics
from scraper.books import search_books, download_books
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

obj = links()
load_dotenv()
TOKEN = environ.get("TOKEN")
SONG = environ.get("SONG")


def start(update, context):
    """Send instructions."""
    chat_id = update.message.chat.id
    message = "You can download books, torrent and srt files from "
    message += "*1337x*, *yts* and *yts-subs*.\n\n"
    message += "Use the following commands to do so.\n\n"
    message += "/torrent - to search for *torrent files*.\n\n"
    message += "/yts - to search for *movies*.\n\n"
    message += "/subs - to search for *subtitles*.\n\n"
    message += "/books - to search for *books*.\n\n"
    message += "/lyrics - to search for *lyrics*.\n\n"
    message += "/games - to search for *games*.\n\n"
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
    message = search_subs(message[0], chatid, obj)
    obj.command(chatid, "subs")
    update.message.reply_text(message)


def mcqs(update, content):
    """Send mcqs pdf url."""
    chatid = update.message.chat.id
    message = update.message.text
    obj.chatid(chatid)
    url = re.findall("/mcqs (.*)", message)
    update.message.reply_text("Please wait.")
    message = generate_pdf(url[0])
    obj.command(chatid, "mcqs")
    update.message.reply_text(message)


def games(update, context):
    """Search for games."""
    chatid = update.message.chat.id
    message = update.message.text
    obj.chatid(chatid)
    message = re.findall("/games (.*)", message)
    message = search_games(chatid, message[0], obj)
    obj.command(chatid, "games")
    update.message.reply_text(message)


def lyrics(update, context):
    """Search for lyrics."""
    chatid = update.message.chat.id
    message = update.message.text
    obj.chatid(chatid)
    message = re.findall("/lyrics (.*)", message)
    message = search_lyrics(chatid, message[0], obj)
    obj.command(chatid, "lyrics")
    update.message.reply_text(message)


def yts(update, context):
    """Search for torrent from yts and send the results to the user."""
    chatid = update.message.chat.id
    obj.chatid(chatid)
    message = update.message.text
    message = re.findall("/yts (.*)", message)
    message = search_yts(message[0], chatid, obj)
    obj.command(chatid, "yts")
    update.message.reply_text(message)


def x(update, context):
    """Search for torrent from 1337x and send the results to the user."""
    chatid = update.message.chat.id
    message = update.message.text
    obj.chatid(chatid)
    message = re.findall("/torrent (.*)", message)
    message = search_1337x(message[0], chatid, obj)
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
    results_len = obj.get_len(chatid)
    message = ""
    command = obj.get_command(chatid)
    try:
        if command == "yts":
            href, message, magnet = get_quality_yts(int(query), chatid, obj)
        elif command == "subs":
            href, message = get_subs(int(query), chatid, obj)
        elif command == "books":
            href, message = download_books(chatid, int(query), obj)
        elif command == "lyrics":
            href, lyrics = get_lyrics(chatid, int(query), obj)
        elif command == "games":
            href, message = get_games(chatid, int(query), obj)
        else:
            href = get_magnet_1337x(int(query), chatid, obj)
        # If the function returns an empty list it means no link is found.
        if href == [] and command != "lyrics":
            text = "Download link not found."
        else:
            text = ""
            if command == "1337x":
                text = "Paste any of the following magnetic link in your"
                text += " torrent client.\n\n"
                for i, link in enumerate(href):
                    text += "{}. {}\n\n".format(i + 1, link)
            elif command == "lyrics":
                text = lyrics
            elif command == "yts":
                yts_reply(href, update, message, magnet)
                return
            else:
                text = "You can download from the following links\n\n"
                for i, link in enumerate(href):
                    # Inline url is created for yts torrent links an not for
                    # 1337x since 1337x returns magnet links
                    # which cannot be used as an inline url in telegram.
                    if(message[i] == "magnet"):
                        text += f"{link}\n"
                    else:
                        text += "[{}]({})\n".format(message[i], link)
    except Exception as e:
        print(e)
        if results_len > 0 and query.isnumeric() and int(query) > results_len:
            text = "Enter a valid choice in the range of the results."
        elif command == "lyrics":
            text = "Lyrics not available!"
        else:
            text = "Enter a valid query\n\nFor eg. /yts Rambo"

    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


def youtube(update, context):
    """Send link of audio file of the youtube video."""
    chatid = update.message.chat.id
    message = update.message.text
    message = re.findall("/youtube (.*)", message)
    ydl_opts = {
        'format': 'bestaudio',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(
            message[0], download=False)
    message = f"[Result]({info['formats'][0]['url']})"
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


def yts_reply(href, update, message, magnet):
    text = "You can download from the following links\n\n"
    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    for i, link in enumerate(href):
        text = f"*Torrent file*:[{message[i]}]({link})\n"
        update.message.reply_text(text,
                                    parse_mode=ParseMode.MARKDOWN)
        text = f"*Magnet link({message[i]})*\n\n"
        update.message.reply_text(text,
                                    parse_mode=ParseMode.MARKDOWN)
        text = f"{magnet[i]}\n\n"
        update.message.reply_text(text,
                                    parse_mode=ParseMode.MARKDOWN)

def main():
    """Initiate bot."""
    updater = Updater(TOKEN, use_context=True)  # Enter your token here
    dp = updater.dispatcher
    # Handlers are created for getting torrent from specified websites.
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('yts', yts))
    dp.add_handler(CommandHandler('torrent', x))
    dp.add_handler(CommandHandler('subs', subs))
    dp.add_handler(CommandHandler('books', books))
    dp.add_handler(CommandHandler('lyrics', lyrics))
    dp.add_handler(CommandHandler('games', games))
    dp.add_handler(CommandHandler('mcqs', mcqs))
    dp.add_handler(CommandHandler('youtube', youtube))
    dp.add_handler(MessageHandler(Filters.text, reply))
    # By default timeout is 0.
    updater.start_polling(timeout=180)
    updater.idle()


if __name__ == '__main__':
    main()
