"""Webscraping functions."""

import re
import requests
from bs4 import BeautifulSoup


def search_yts(name, chatid, obj):
    """Search from yts."""
    obj.reset(chatid)

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
        for i, result in enumerate(results):
            title = result['oldtitle']
            url = result['href']
            obj.add(chatid, i + 1, title, url, 0)
        message = obj.build_message(chatid)
    return message


def get_quality_yts(choice, chatid, obj):
    """Download torrent from yts based on quality."""
    url = obj.get_url(chatid, int(choice))
    # If seeds are present that means the data is from 1337x so this function
    # returns empty values.
    if obj.get_seeds(chatid, int(choice)):
        return [], ""

    href = []
    message = []

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        results = soup.findAll('a',
                               attrs={'class': 'lnk-lnk',
                                      'rel': 'nofollow',
                                      'href': re.compile('https://yts(.*)')
                                      }
                               )

        for result in results:
            href.append(result['href'])
            message.append(result.findAll('span',
                                          attrs={'class': 'lnk lnk-dl'},
                                          text=re.compile('([720][1080])*')
                                          )[0].text)

    except Exception as e:
        print(e)

    return href, message
