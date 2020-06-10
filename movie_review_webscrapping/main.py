import traceback
from concurrent.futures import ProcessPoolExecutor as Pool

import numpy as np
import requests
from bs4 import BeautifulSoup
from lxml import html

from config import config
from data_storage.data_storage import Database


def get_soup(url):
    return BeautifulSoup(requests.get(url, headers=config.HEADERS).content, 'html.parser')


def get_text_from_xpath(page, xpath):
    tree = html.fromstring(page.content)
    try:
        rating = tree.xpath(xpath)[0].text
    except IndexError:
        rating = np.NaN
    return rating


class Review(Database):

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
            id_dict = {}
            value = imdb_id.find('a')
            self.ids.append(value.get_text() + '|' + (str(value)[16:25]))
            id_dict['title'] = value.get_text()
            id_dict['imdb_id'] = str(value)[16:25]
            self.dict_list.append(id_dict)

        return self.dict_list

    @staticmethod
    def get_reviews(ids):
        review = []
        try:
            title, imdb_id = ids.split("|")

            good_review_url = config.GOOD_REVIEW_URL.replace('{id}', imdb_id)
            bad_review_url = config.BAD_REVIEW_URL.replace('{id}', imdb_id)

            good_soup = get_soup(good_review_url)
            good_review_list = [element.get_text() for element in
                                good_soup.find_all('div', {'class': 'text show-more__control'})]
            good_page = requests.get(good_review_url)
            good_rating_list = [
                get_text_from_xpath(good_page, f'(//span[@class="rating-other-user-rating"]//span[1])[{i}]')
                for i in range(0, len(good_review_list))]

            bad_soup = get_soup(bad_review_url)
            bad_review_list = [element.get_text() for element in
                               bad_soup.find_all('div', {'class': 'text show-more__control'})]
            bad_page = requests.get(bad_review_url)
            bad_rating_list = [
                get_text_from_xpath(bad_page, f'(//span[@class="rating-other-user-rating"]//span[1])[{i}]')
                for i in range(0, len(bad_review_list))]

            for i in range(len(good_rating_list)):
                temp_dict = dict()
                temp_dict = {'name': title, 'review': good_review_list[i], 'ratings': good_rating_list[i]}
                review.append(temp_dict)

            for i in range(len(bad_rating_list)):
                temp_dict = dict()
                temp_dict = {'name': title, 'review': bad_review_list[i], 'ratings': bad_rating_list[i]}
                review.append(temp_dict)

            config.logger.info(f'Title - {title}')
            config.logger.info(f'Good Reviews - {len(good_review_list)}')
            config.logger.info(f'Good Reviews - {len(good_rating_list)}')
            config.logger.info(f'Bad Reviews - {len(bad_review_list)}')
            config.logger.info(f'Good Reviews - {len(bad_rating_list)}')

        except (AttributeError, KeyError) as e:
            config.logger.error(traceback.format_exc())
            config.logger.error('Error has occurred in get_reviews =====>' + e)

        return review


def fetch_reviews(review):
    try:
        with Pool(max_workers=config.MAX_WORKERS) as inner_pool:
            rs = inner_pool.map(review.get_reviews, review.ids)
    except Exception as e:
        config.logger.error(f'Exception occurred in fetch_reviews method - {e}')
    finally:
        inner_pool.shutdown()
    review.reviews = list(rs)


def perform_scrapping(movie_series_dict):
    for rated_type, url in movie_series_dict.items():
        obj = Review(url)

        if 'top' in rated_type:
            obj.load_tags('top')
        else:
            obj.load_tags('bottom')

        obj.load_imdb_ids()

        fetch_reviews(obj)

        obj.store_data('imdb_id', obj.dict_list)
        obj.store_data_with_list_of_list('reviews', obj.reviews)

        print(f'Finished scrapping and stored {rated_type}')
        config.logger.info(f'Finished scrapping and stored {rated_type}')


def start(movie_series_dict):
    try:
        with Pool(max_workers=config.MAX_WORKERS) as outer_pool:
            outer_pool.map(perform_scrapping, movie_series_dict)
    except Exception as e:
        config.logger.error(f'Exception occurred in start method - {e}')
    finally:
        outer_pool.shutdown()
