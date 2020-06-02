from datetime import datetime
from multiprocessing import Pool
from pprint import pprint

import numpy as np
import requests
from bs4 import BeautifulSoup

import config

reviews = {}


def get_content(url1):
    return BeautifulSoup(requests.get(url1, headers=config.HEADERS).content, 'html.parser')


def get_all_reviews(review, title):
    reviews[title] = reviews[title] + '||' + review.getText()


def get_reviews(movie):
    title, id = movie.split("|")
    soup = get_content(config.REVIEW_URL.replace('{id}', id))
    try:
        review_list = soup.find_all('div', {'class': 'text show-more__control'})
        print(review_list.size())
        for review in review_list:
            reviews[title] = reviews[title] + '||' + review.getText()
    except (AttributeError, KeyError) as e:
        reviews[title] = reviews[title] + '||' + np.NaN
    print(title)


if __name__ == '__main__':
    start = datetime.now()

    soup = get_content(config.MOVIES_HOME_URL)
    movie_tags = soup.findAll('td', {'class': 'titleColumn'})

    movie_ids = []
    for id in movie_tags:
        value = id.find('a')
        movie_ids.append(value.get_text() + '|' + (str(value)[16:25]))

    pprint(movie_ids)
    pool = Pool()
    pool.map(get_reviews, movie_ids)
    pprint(reviews)
    finish = datetime.now()
    print(finish - start)
