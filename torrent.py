"""Webscraping functions."""

import requests
from bs4 import BeautifulSoup
import re


def search(name, obj):
    """Search from yts."""
    obj.reset()

    try:
        name = name.replace(" ", "+")
    except Exception as e:
        print(e)
        pass

    url = "https://ytsnew.com/?s=" + name
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    results = soup.findAll('a', attrs={'class': 'ml-mask'})

    if results == []:
        message = "No result found"
    else:
        i = 1
        for result in results:
            title = result['oldtitle']
            url = result['href']
            obj.add(i, title, url, 0)
            i += 1
        message = obj.build_message()

    return message


def quality(choice, obj):
    """Download torrent from yts based on quality."""
    url = obj.get_url(int(choice))

    # If seeds are present that means the data is from 1337x so this function
    # returns empty values.
    if obj.get_seeds(int(choice)):
        return [], ""

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    results = soup.findAll('a',
                           attrs={'class': 'lnk-lnk',
                                  'rel': 'nofollow',
                                  'href': re.compile('https://yts(.*)')
                                  }
                           )
    href = []
    message = []

    for result in results:
        href.append(result['href'])
        message.append(result.findAll('span',
                                      attrs={'class': 'lnk lnk-dl'},
                                      text=re.compile('([720][1080])*')
                                      )[0].text)

    return href, message


def search_1337x(search, obj):
    """Search from 1337x."""
    obj.reset()
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
            obj.add(i, link.text, link['href'], seed.text)
            i += 1
        message = obj.build_message()

    return message


def get_magnet_1337x(choice, obj):
    """Get magnet link from 1337x."""
    url = 'https://www.1377x.to' + obj.get_url(int(choice))
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.content, 'html5lib')
    magnets = soup.findAll('a', attrs={'href': re.compile('magnet(.*)')})
    href = []

    for magnet in magnets:
        href.append(magnet['href'])

    return href
