import requests
from bs4 import BeautifulSoup
import re
from movies import movies

def search(name,obj):
    obj.reset()
    try:
        name = name.replace(" ","+")
    except:
        pass
    url = "https://ytson.com/?s="+name
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    results = soup.findAll('a',attrs = {'class': 'ml-mask'})#'browse-movie-title'})
    i = 1
    if results == []:
        message = "No result found"
    else:
        for result in results:
            title = result['oldtitle']
            url = result['href']
            obj.add(i,title,url)
            i += 1
        message = obj.build_message()
    return message

def quality(choice,obj):
    url = obj.get_url(int(choice))
    #print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    results = soup.findAll('a',attrs = {'class' : 'lnk-lnk','rel' : 'nofollow','href' : re.compile('https://yts(.*)')})
    href = []
    message = []
    for result in results:
        href.append(result['href'])
        message.append(result.findAll('span',attrs = {'class' : 'lnk lnk-dl'},text = re.compile('([720][1080])*'))[0].text)
    return href,message
