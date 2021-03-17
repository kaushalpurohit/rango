"""Webscraping functions."""

import requests

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 \
                Safari/537.36"}


def search_yts(name, chatid, obj):
    """Search from yts."""
    obj.reset(chatid)

    url = "https://yts.mx/api/v2/list_movies.json?query_term=" + name
    response = requests.get(url, verify=False, headers=headers).json()
    for i, result in enumerate(response["data"]["movies"]):
        title_long = result['title_long']
        _id = result['id']
        title = result['title']
        obj.add_yts(chatid, i + 1, title_long, _id, title)
    message = obj.build_message_yts(chatid)
    return message


def get_quality_yts(choice, chatid, obj):
    """Download torrent from yts based on quality."""
    _id = obj.get_id(chatid, int(choice))
    title = obj.get_title(chatid, int(choice))
    url = "https://yts.mx/api/v2/movie_details.json?movie_id=" + str(_id)
    # If seeds are present that means the data is from 1337x so this function
    # returns empty values.

    href = []
    message = []
    magnet = []

    try:
        response = requests.get(url, headers=headers).json()
        for result in response['data']['movie']['torrents']:
            href.append(result['url'])
            _hash = result['hash']
            quality = result['quality']
            message.append(quality)
            magnet_link = f"magnet:?xt=urn:btih:{_hash}&dn={title}&tr="
            magnet_link += "http://track.one:1234/announce&tr="
            magnet_link += "udp://track.two:80"
            magnet.append(magnet_link)

    except Exception as e:
        print(e)

    return href, message, magnet
