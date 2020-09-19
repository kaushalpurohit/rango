import requests
from bs4 import BeautifulSoup
import re
from movies import movies

url = "https://ytson.com/?s=fast+and+the+furious"#"http://yts.lt/browse-movies/fast/all/all/0/latest/0/all"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html5lib')
results = soup.findAll('a',attrs = {'class': 'ml-mask'})#'browse-movie-title'})
obj = movies()
i = 1
for result in results:
    title = result['oldtitle']
    url = result['href']
    obj.add(i,title,url)
    i += 1
obj.build_message()
message = obj.get_message()
print(message)
choice = input("Enter choice:")
url = obj.get_url(int(choice))
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html5lib')
results = soup.findAll('a',attrs = {'class' : 'lnk-lnk','rel' : 'nofollow','href' : re.compile('https://yts(.*)')})
for result in results:
    print(result.findAll('span',text = re.compile('[720][1080]*'))[0].text,result['href']+"\n")