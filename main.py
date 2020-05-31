import requests
from bs4 import BeautifulSoup
from pprint import pprint


url = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

page = requests.get(url, headers = headers)

soup = BeautifulSoup(page.content, 'html.parser')
movie_tags = soup.findAll('td', {'class': 'titleColumn'})

movie_ids = {}
for id in movie_tags:
    value = id.find('a')
    movie_ids[value.get_text()] = str(value)[16:25]

# print(movie_ids)

reviewURL = 'https://www.imdb.com/title/{id}/reviews?ref_=tt_urv'
reviews = {}
i = 0
for title, movie_id in movie_ids.items():
    page = requests.get(reviewURL.replace('{id}', movie_id), headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    reviews[title] = soup.find('div', {'class': 'text show-more__control'}).get_text()
    i += 1
    if(i == 25):
        break
pprint(reviews)



