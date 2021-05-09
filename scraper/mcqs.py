"""Scrape sanfoundry."""

import requests
import pdfkit
from os import environ, remove
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
FILEIO_KEY = environ.get("FILEIO_KEY")
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 \
                Safari/537.36"}


def get_source(url, final_body):
    """Get source code."""
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html5lib')
    body = soup.findAll('div', attrs={'class': 'entry-content'})[0]
    try:
        next_url_div = body.findAll('div', attrs={'class': 'sf-nav-bottom'})[1]
        next_url = next_url_div.a['href']
    except TypeError:
        final_body += str(body)
        return final_body
    final_body += str(body)
    final_body = get_source(next_url, final_body)
    return final_body


def generate_pdf(href):
    """Generate pdf file."""
    final_body = ""
    url = "https://www.sanfoundry.com" + href
    final_body = get_source(url, final_body)
    f = open("/tmp/test.html", "w")
    f.write(final_body)
    options = {
        "enable-local-file-access": None
    }
    try:
        pdfkit.from_file('/tmp/test.html', '/tmp/final.pdf', options=options)
    except OSError as e:
        if 'Done' not in str(e):
            raise e
    headers = {
        "Authorization": f"Bearer {FILEIO_KEY}"
    }
    data = {
        "file": open("/tmp/final.pdf", 'rb')
    }
    upload_url = "https://file.io/"
    response = requests.post(upload_url, files=data, headers=headers).json()
    return response["link"]


if __name__ == '__main__':
    url = "https://www.sanfoundry.com/embedded-systems-questions-answers-processor-embedded-system/"
    final_body = ""
    final_body = get_source(url, final_body)
    f = open("../files/test.html", "w")
    f.write(final_body)
    options = {
        "enable-local-file-access": None
    }
    try:
        pdfkit.from_file('../files/test.html', '../files/final.pdf', options=options)
    except OSError as e:
        if 'Done' not in str(e):
            raise e
    headers = {
        "Authorization": f"Bearer {FILEIO_KEY}"
    }
    data = {
        "file": open("/home/kaushal/yts-tele-bot/files/final.pdf", 'rb')
    }
    upload_url = "https://file.io/"
    response = requests.post(upload_url, files=data, headers=headers).json()
    print(response["link"])
    remove("../files/final.pdf")
