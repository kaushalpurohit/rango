"""Yts-subs scraping functions."""

import re
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 \
                Safari/537.36"}


def search_subs(search, chatid, obj):
    """Search subtitles."""
    obj.reset(chatid)
    url = "https://yts-subs.com/search/" + search
    reponse = requests.get(url, headers=headers)
    soup = BeautifulSoup(reponse.content, 'html5lib')
    results = soup.findAll('div', attrs={'class': 'media-body'})

    for i, result in enumerate(results):
        href = result.find('a')['href']
        title = result.find('h3').text
        info = result.findAll('span', attrs={'class': 'movinfo-section'})
        year = info[0].text.strip()
        year = re.findall("[0-9]+", year)
        title = f"{title} ({year[0]})"
        obj.add(chatid, i + 1, title, href, None)
    message = obj.build_message(chatid)
    return message


def get_subs(choice, chatid, obj):
    """Return subtitle download links."""
    url = "https://yts-subs.com" + obj.get_url(chatid, int(choice))
    try:
        reponse = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
        raise Exception("Invalid url")
    soup = BeautifulSoup(reponse.content, 'html5lib')
    table = soup.find('tbody')
    results = table.findAll('tr')
    href = []
    message = []
    for i, result in enumerate(results):
        link = result.find('a')['href']
        link = link.replace('subtitles', 'subtitle')
        language = result.findAll('td', {'class': 'flag-cell'})[0].text.strip()
        title = result.find('a').text.strip()
        title = re.findall("subtitle (.*)", title)[0]
        title = re.sub(r'(\[.*\])', '', title)
        title = f"{language}: {title}"
        link = f"https://yifysubtitles.org{link}.zip"
        href.append(link)
        message.append(title)
        if(i == 55):
            break
    return href, message
