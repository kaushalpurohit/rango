"""Search and get lyrics."""

# import re
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 \
                Safari/537.36"}


def search_lyrics(chatid, song, obj):
    """Search for lyrics."""
    obj.reset(chatid)
    url = "https://genius.com/api/search/song?q=" + song
    response = requests.get(url, headers=headers).json()
    for i, data in enumerate(response['response']['sections'][0]['hits']):
        result = data['result']
        title = result['full_title']
        link = result['path']
        obj.add(chatid, i + 1, title, link, None)
    message = obj.build_message(chatid)
    return message


def get_lyrics(chatid, choice, obj):
    """Get lyrics."""
    url = "https://genius.com/amp" + obj.get_url(chatid, int(choice))
    reponse = requests.get(url, headers=headers)
    soup = BeautifulSoup(reponse.content, 'html5lib')
    lyrics = soup.findAll('div', attrs={'class': 'lyrics'})[0].text
    return [], lyrics
