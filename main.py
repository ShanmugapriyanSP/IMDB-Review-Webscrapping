from pprint import pprint

import requests
from bs4 import BeautifulSoup

url = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}


def get_content(url):
    return BeautifulSoup(requests.get(url, headers=HEADERS).content, 'html.parser')


soup = get_content(url)
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
    soup = get_content(reviewURL.replace('{id}', movie_id))
    reviews[title] = soup.find('div', {'class': 'text show-more__control'}).get_text()
    i += 1
    if (i == 25):
        break
pprint(reviews)
