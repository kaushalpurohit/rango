"""Search for books and download functions."""

import re
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 \
                Safari/537.36"}


def search_books(chatid, book_name, obj):
    """Search for books."""
    obj.reset(chatid)
    url = "https://www.pdfdrive.com/search?q={}".format(book_name)

    source = requests.get(url, headers=headers)
    soup = BeautifulSoup(source.content, 'html5lib')
    results = soup.findAll('a', attrs={'class': 'ai-search'})

    for i, result in enumerate(results):
        title = result.find('h2').text
        link = result['href']
        obj.add(chatid, i + 1, title, link, None)

    message = obj.build_message(chatid)
    return message


def download_books(chatid, choice, obj):
    """Return download link."""
    url = "https://www.pdfdrive.com" + obj.get_url(chatid, int(choice))
    title = obj.get_title(chatid, int(choice))
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, 'html5lib')

    bookId = soup.find('button', attrs={'id': 'previewButtonMain'})['data-id']
    session = re.findall(r'session=(.+?)"', str(soup))[0]

    url = f"https://www.pdfdrive.com/download.pdf?id={bookId}&h={session}"
    url_list = list()
    url_list.append(url)
    title_list = list()
    title_list.append(title)

    return url_list, title_list
