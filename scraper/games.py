"""fitgirlrepacks scraping functions."""

# import re
import requests
from bs4 import BeautifulSoup


def search_games(chatid, search, obj):
    """Search for games."""
    obj.reset(chatid)
    url = "https://fitgirlrepacks.co/search/" + search
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    results = soup.findAll('h2', attrs={'class': 'entry-title'})
    for i, result in enumerate(results):
        tag = result.find('a')
        title = tag.text
        link = tag['href']
        obj.add(chatid, i + 1, title, link, None)
    message = obj.build_message(chatid)
    return message
