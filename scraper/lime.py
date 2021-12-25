"""lime torrent scraping functions."""

import re
import requests
from bs4 import BeautifulSoup
import json

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 \
                Safari/537.36"}

def search_lime(search):
    """Search from lime."""
    # obj.reset(chatid)
    url = f"https://ww2.limetorrents.cyou/api.php?url=/q.php?q={search}&cat=0"
    response = requests.get(url, headers=headers)
    torrents = response.json()
    for i, torrent in enumerate(torrents):
        print(torrent['name'])

search_lime(input())