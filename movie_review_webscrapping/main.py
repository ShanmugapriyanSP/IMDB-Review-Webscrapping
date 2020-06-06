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

    def load_tags(self, rated='top'):
        if rated == 'top':
            self.tags = self.soup.findAll('td', {'class': 'titleColumn'})
        elif rated == 'bottom':
            self.tags = self.soup.findAll('div', {'class': 'col-title'})

    def load_imdb_ids(self):
        for imdb_id in self.tags:
            dict = {}
            value = imdb_id.find('a')
            self.ids.append(value.get_text() + '|' + (str(value)[16:25]))
            dict['title'] = value.get_text()
            dict['imdb_id'] = str(value)[16:25]
            self.dict_list.append(dict)

        return self.dict_list


def get_reviews(ids):
    review = {}
    try:
        title, imdb_id = ids.split("|")

        good_review_url = config.GOOD_REVIEW_URL.replace('{id}', imdb_id)
        bad_review_url = config.BAD_REVIEW_URL.replace('{id}', imdb_id)

        good_soup = get_soup(good_review_url)
        good_review_list = [element.get_text() for element in
                            good_soup.find_all('div', {'class': 'text show-more__control'})]
        good_page = requests.get(good_review_url)
        good_rating_list = [get_text_from_xpath(good_page, f'(//span[@class="rating-other-user-rating"]//span[1])[{i}]')
                            for i in range(0, len(good_review_list))]

        bad_soup = get_soup(bad_review_url)
        bad_review_list = [element.get_text() for element in
                           bad_soup.find_all('div', {'class': 'text show-more__control'})]
        bad_page = requests.get(bad_review_url)
        bad_rating_list = [get_text_from_xpath(bad_page, f'(//span[@class="rating-other-user-rating"]//span[1])[{i}]')
                           for i in range(0, len(bad_review_list))]

        review['name'] = title
        review['review'] = good_review_list
        review['review'].extend(bad_review_list)
        review['ratings'] = good_rating_list
        review['ratings'].extend(bad_rating_list)
        config.logger.info('Title =====>' + title)
        config.logger.info('Good Reviews =====>' + str(len(good_review_list)))
        config.logger.info('Bad Reviews =====>' + str(len(bad_review_list)))
        config.logger.info('Good Rating =====>' + str(len(good_rating_list)))
        config.logger.info('Bad Rating =====>' + str(len(bad_rating_list)))
    except (AttributeError, KeyError) as e:
        config.logger.error('Error has occurred in get_reviews =====>' + e)
        review['name'] = title
        review['review'].extend(np.NaN)
        review['ratings'].extend(np.NaN)
    return review


def fetch_reviews(review):
    pool = Pool(processes=multiprocessing.cpu_count())
    rs = pool.map(get_reviews, review.ids)
    review.reviews = rs
    pool.close()
    pool.join()


def start():
    start_time = datetime.now()

    movies_top = Review(config.MOVIES_TOP_URL)
    series_top = Review(config.SERIES_TOP_URL)
    movies_bottom = Review(config.MOVIES_BOTTOM_URL)
    series_bottom = Review(config.SERIES_BOTTOM_URL)

    movies_top.load_tags('top')
    series_top.load_tags('top')
    movies_bottom.load_tags('bottom')
    series_bottom.load_tags('bottom')

    movies_top.load_imdb_ids()
    series_top.load_imdb_ids()
    movies_bottom.load_imdb_ids()
    series_bottom.load_imdb_ids()

    fetch_reviews(movies_top)
    fetch_reviews(series_top)
    fetch_reviews(movies_bottom)
    fetch_reviews(series_bottom)

    data_storage.store_data(movies_top.dict_list, 'imdb_movie_id')
    data_storage.store_data(movies_top.reviews, 'movie_reviews')
    data_storage.store_data(series_top.dict_list, 'imdb_series_id')
    data_storage.store_data(series_top.reviews, 'series_reviews')
    data_storage.store_data(movies_bottom.dict_list, 'imdb_movie_id')
    data_storage.store_data(movies_bottom.reviews, 'movie_reviews')
    data_storage.store_data(series_bottom.dict_list, 'imdb_series_id')
    data_storage.store_data(series_bottom.reviews, 'series_reviews')

    finish_time = datetime.now()

    print(finish_time - start_time)
