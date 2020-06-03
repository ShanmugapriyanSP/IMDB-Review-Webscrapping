from datetime import datetime
from multiprocessing import Pool

import numpy as np
import requests
from bs4 import BeautifulSoup

from config import config
from data_storage import data_storage


def get_content(url1):
    return BeautifulSoup(requests.get(url1, headers=config.HEADERS).content, 'html.parser')


def get_reviews(movie):
    review = {}
    title, id = movie.split("|")
    soup = get_content(config.REVIEW_URL.replace('{id}', id))
    try:
        review_list = [element.get_text() for element in soup.find_all('div', {'class': 'text show-more__control'})]
        review['movie_name'] = title
        review['movie_review'] = review_list
        config.logger.info('Title =====>' + title)
        config.logger.info('Total Reviews =====>' + str(len(review_list)))
    except (AttributeError, KeyError) as e:
        review[title] = review[title].append(np.NaN)
    return review


if __name__ == '__main__':
    start = datetime.now()

    soup = get_content(config.MOVIES_HOME_URL)
    movie_tags = soup.findAll('td', {'class': 'titleColumn'})

    movie_ids = []
    for id in movie_tags:
        value = id.find('a')
        movie_ids.append(value.get_text() + '|' + (str(value)[16:25]))

    pool = Pool()
    reviews = pool.map(get_reviews, movie_ids)

    finish = datetime.now()
    print(finish - start)

    data_storage.store_data(reviews)
