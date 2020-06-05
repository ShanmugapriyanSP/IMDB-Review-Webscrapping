import multiprocessing
from datetime import datetime
from multiprocessing import Pool

import numpy as np
import requests
from bs4 import BeautifulSoup
from lxml import html

from config import config
from data_storage import data_storage


def get_soup(url):
    return BeautifulSoup(requests.get(url, headers=config.HEADERS).content, 'html.parser')


def get_text_from_xpath(page, xpath):
    tree = html.fromstring(page.content)
    try:
        rating = tree.xpath(xpath)[0].text
    except IndexError:
        rating = np.NaN
    return rating


class Review:

    def __init__(self, url):
        self.url = url
        self.soup = get_soup(url)
        self.ids = []
        self.tags = []
        self.reviews = []
        self.dict_list = []

    def load_tags(self):
        self.tags = self.soup.findAll('td', {'class': 'titleColumn'})

    def load_imdb_ids(self):
        for id in self.tags:
            dict = {}
            value = id.find('a')
            self.ids.append(value.get_text() + '|' + (str(value)[16:25]))
            dict['title'] = value.get_text()
            dict['imdb_id'] = str(value)[16:25]
            self.dict_list.append(dict)

        return self.dict_list


def get_reviews(ids):
    review = {}
    try:
        title, imdb_id = ids.split("|")
        review_url = config.REVIEW_URL.replace('{id}', imdb_id)
        soup = get_soup(review_url)
        review_list = [element.get_text() for element in
                       soup.find_all('div', {'class': 'text show-more__control'})]
        page = requests.get(review_url)
        rating_list = [get_text_from_xpath(page, f'(//span[@class="rating-other-user-rating"]//span[1])[{i}]')
                       for i in range(0, len(review_list) + 1)]
        review['name'] = title
        review['review'] = review_list
        review['ratings'] = rating_list
        config.logger.info('Title =====>' + title)
        config.logger.info('Total Reviews =====>' + str(len(review_list)))
        config.logger.info('Total Reviews =====>' + str(len(rating_list)))
    except (AttributeError, KeyError) as e:
        config.logger.error('Error has occurred in get_reviews =====>' + e)
        review['name'] = title
        review['review'] = np.NaN
    return review


def run(review):
    pool = Pool(processes=multiprocessing.cpu_count())
    rs = pool.map(get_reviews, review.ids)
    review.reviews = rs
    pool.close()
    pool.join()


def start():
    start_time = datetime.now()

    movies = Review(config.MOVIES_HOME_URL)
    series = Review(config.SERIES_HOME_URL)

    movies.load_tags()
    series.load_tags()

    movies.load_imdb_ids()
    series.load_imdb_ids()

    run(movies)
    run(series)

    data_storage.store_data(movies.dict_list, 'imdb_movie_id')
    data_storage.store_data(movies.reviews, 'movie_reviews')
    data_storage.store_data(series.dict_list, 'imdb_series_id')
    data_storage.store_data(series.reviews, 'series_reviews')

    finish_time = datetime.now()

    print(finish_time - start_time)
