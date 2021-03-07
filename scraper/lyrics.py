"""Search and get lyrics."""

# import re
import requests
from bs4 import BeautifulSoup


def search_lyrics(chatid, song, obj):
    """Search for lyrics."""
    obj.reset(chatid)
    url = "https://genius.com/api/search/song?q=" + song
    response = requests.get(url).json()
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
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.content, 'html5lib')
    lyrics = soup.findAll('div', attrs={'class': 'lyrics'})[0].text
    return [], lyrics
