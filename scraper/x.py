"""1337x scraping functions."""

import re
import requests
from bs4 import BeautifulSoup


def search_1337x(search, chatid, obj):
    """Search from 1337x."""
    obj.reset(chatid)
    url = f'https://www.1377x.to/search/{search}/1'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    href = soup.findAll('a', attrs={'href': re.compile('/torrent/(.*)')})
    seeds = soup.findAll('td', attrs={'class': 'seeds'})

    if href == []:
        message = "No results found"
    else:
        i = 1
        for (link, seed) in zip(href, seeds):
            obj.add(chatid, i, link.text, link['href'], seed.text)
            i += 1
        message = obj.build_message(chatid)

    return message


def get_magnet_1337x(choice, chatid, obj):
    """Get magnet link from 1337x."""
    url = 'https://www.1377x.to' + obj.get_url(chatid, int(choice))
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.content, 'html5lib')
    magnets = soup.findAll('a', attrs={'href': re.compile('magnet(.*)')})
    href = []

    for magnet in magnets:
        href.append(magnet['href'])

    return href
