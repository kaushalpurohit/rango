"""fitgirlrepacks scraping functions."""

import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 \
                Safari/537.36"}


def search_games(chatid, search, obj):
    """Search for games."""
    obj.reset(chatid)
    url = "https://fitgirlrepacks.co/search/" + search
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html5lib')
    results = soup.findAll('h2', attrs={'class': 'entry-title'})
    for i, result in enumerate(results):
        tag = result.find('a')
        title = tag.text
        link = tag['href']
        obj.add(chatid, i + 1, title, link, None)
    if results != []:
        message = obj.build_message(chatid)
    else:
        message = "No results found."
    return message


def get_games(chatid, choice, obj):
    """Get download link."""
    url = obj.get_url(chatid, int(choice))
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html5lib')
    content = soup.findAll('div', attrs={'class': 'entry-content'})[0]
    download_links_block = content.find('li')
    download_links = download_links_block.findAll('a')
    href = []
    message = []
    for link in download_links:
        text = link.text
        link = link['href']
        href.append(link)
        message.append(text)
    return href, message
