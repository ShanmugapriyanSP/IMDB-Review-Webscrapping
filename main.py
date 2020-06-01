from datetime import datetime
from multiprocessing import Pool
from pprint import pprint

import numpy as np
import requests
from bs4 import BeautifulSoup

import config


def get_content(url1):
    return BeautifulSoup(requests.get(url1, headers=config.HEADERS).content, 'html.parser')


def get_reviews(movie):
    review = {}
    title, id = movie.split("---")
    soup = get_content(config.REVIEW_URL.replace('{id}', id))
    try:
        review[title] = soup.find('div', {'class': 'text show-more__control'}).get_text()
    except AttributeError:
        review[title] = np.NaN
    print(title)
    return review


if __name__ == '__main__':
    start = datetime.now()

    soup = get_content(config.URL)
    movie_tags = soup.findAll('td', {'class': 'titleColumn'})

    movie_ids = []
    for id in movie_tags:
        value = id.find('a')
        movie_ids.append(value.get_text() + '---' + (str(value)[16:25]))

    pprint(movie_ids)
    pool = Pool()
    reviews = pool.map(get_reviews, movie_ids)
    pprint(reviews)
    finish = datetime.now()
    print(finish - start)
