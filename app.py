"""
Telegram bot to download books from pdfdrive.com
"""

import json
import requests
import time
from yts import search,quality
from movies import movies
import urllib

TOKEN = "1250079555:AAGxMQFXbCTR7hQCFcc7uLXzCYMyvEiTCU8" # Bot token
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
obj = movies()

def get_response(url):
    response = requests.get(url)
    content = response.content.decode("UTF-8")
    return content

def get_json_from_url(url):
    content = get_response(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):

    url = URL + "getUpdates?timeout=100"

    if offset:
        url += "&offset={}".format(offset)

    js = get_json_from_url(url)
    return js

def get_last_chat_id_and_text(updates):
    """checks for last text and chat id and returns the same"""

    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def get_last_update_id(updates):
    """Checks for last update id and returns the latest update id"""

    update_ids = []

    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))

    return max(update_ids)

def echo_all(updates):
    """iterates over updates"""
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            is_int = True
            try:
                int(text)
            except ValueError:
                is_int = False
            if is_int: # if the user's reponse is an integer download fucntion is called
                message = "Please wait."
                send_message(message,chat)
                href,message = quality(int(text),obj)
                i = 0
                text = "You can download the torrent from the links below\n\n"
                for link in href:
                    text += "{}:{}\n\n".format(message[i],link)
                    i += 1
                send_message(text,chat)
            else:
                if text == "/start":
                    message = "Hi! I am the yts bot.\n"
                    message += "Enter a movie name"
                else:
                    message = search(text,obj)          
                send_message(message, chat)
                break

        except Exception as e:
            print(e)

def send_file(file,chat):
    url = URL + "sendDocument?document={}&chat_id={}".format(file,chat)
    get_response(url)

def send_message(text, chat_id):
    text = text.replace("&","and")
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_response(url)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1 # increments update id
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
