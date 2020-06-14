"""
Heart of the application
"""
import time
import traceback
from concurrent.futures import ProcessPoolExecutor as Pool

import numpy as np
import requests
from bs4 import BeautifulSoup
from lxml import html

import config
from data_storage.data_storage import Database


def wait(seconds):
    """
    Simple python wait
    :param seconds
    """
    time.sleep(seconds)


def get_soup(url):
    """
    To parse HTML
    :param Url to parse
    :return soup object for the provied url
    """
    # wait(0.5)
    return BeautifulSoup(requests.get(url, headers=config.HEADERS).content, 'html.parser')


def get_text_from_xpath(page, xpath):
    """
    To get text from a xpath
    :param Page content and xpath to extract text
    :return Extracted text
    """
    tree = html.fromstring(page.content)
    try:
        rating = tree.xpath(xpath)[0].text
    except IndexError:
        rating = np.NaN
    return rating


class Review:
    """
    Class for web scrapping reviews
    """

    def __init__(self, url):
        self.url = url
        self.soup = get_soup(url)
        self.tags = []

    def load_tags(self, rated='top'):
        """
        Fetching movie or series names
        :param rated type differentiating the attributes to
        capture the movie or series titles
        """
        if rated == 'top':
            self.tags = self.soup.findAll('td', {'class': 'titleColumn'})
        elif rated == 'bottom':
            self.tags = self.soup.findAll('div', {'class': 'col-title'})

    def get_distinct_imdb_ids(self):
        """
        To get the imdb unique ids
        :return: String with pipe separating imdb id and title
        """
        ids = []
        for imdb_id in self.tags:
            value = imdb_id.find('a')
            ids.append((str(value)[16:25] + '|' + value.get_text()))
        return ids


class MyDictionary(dict):
    """
    User definded Dictionary class
    """
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


def get_reviews(ids):
    """
    Method to web scrap the reviews with imdb ids.
    It will scrap the reviews and corresponding rating in a
    dictionary and will return back as list of dictionary.

    :param title and imdb ids
    :return review-ratings dictionary as list
    """
    reviews = []
    try:
        title, imdb_id = ids.split("|")

        good_review_url = config.GOOD_REVIEW_URL.replace('{id}', imdb_id)
        bad_review_url = config.BAD_REVIEW_URL.replace('{id}', imdb_id)

        good_soup = get_soup(good_review_url)
        good_review_list = [element.get_text() for element in
                            good_soup.find_all('div', {'class': 'text show-more__control'})]
        good_page = requests.get(good_review_url)
        good_rating_list = [get_text_from_xpath(
            good_page,
            f'(//span[@class="rating-other-user-rating"]//span[1])[{i}]')
            for i in range(0, len(good_review_list))]

        bad_soup = get_soup(bad_review_url)
        bad_review_list = [element.get_text() for element in

                           bad_soup.find_all('div', {'class': 'text show-more__control'})]
        bad_page = requests.get(bad_review_url)
        bad_rating_list = [get_text_from_xpath(
            bad_page,
            f'(//span[@class="rating-other-user-rating"]//span[1])[{i}]')
            for i in range(0, len(bad_review_list))]
        if len(good_rating_list) != 0:
            for review, rating in zip(good_review_list, good_rating_list):
                temp_dict = dict()
                temp_dict = {'name': title,
                             'review': review,
                             'ratings': rating}
                reviews.append(temp_dict)
        else:
            temp_dict = {'name': title,
                         'review': np.NaN,
                         'ratings': np.NaN
                         }
            reviews.append(temp_dict)

        if len(bad_review_list) != 0:
            for review, rating in zip(bad_review_list, bad_rating_list):
                temp_dict = dict()
                temp_dict = {'name': title,
                             'review': review,
                             'ratings': rating}
                reviews.append(temp_dict)
        else:
            temp_dict = {'name': title,
                         'review': np.NaN,
                         'ratings': np.NaN
                         }
            reviews.append(temp_dict)

        config.logger.info(f'Title - {title}')
        config.logger.info(f'Good Reviews - {len(good_review_list)}')
        config.logger.info(f'Good Reviews - {len(good_rating_list)}')
        config.logger.info(f'Bad Reviews - {len(bad_review_list)}')
        config.logger.info(f'Good Reviews - {len(bad_rating_list)}')

    except (AttributeError, KeyError) as exc:
        config.logger.error(traceback.format_exc())
        config.logger.error('Error has occurred in get_reviews =====>' + exc)

    return reviews


def fetch_reviews(ids):
    """
    Fetching reviews with ids along with multi
    processing module

    :param title and imdb ids
    :return review-ratings dictionary as list
    """
    try:
        with Pool(max_workers=config.MAX_WORKERS) as executor:
            review_list = executor.map(get_reviews, ids)
    except Exception as exc:
        config.logger.error(f'Exception occurred in fetch_reviews method - {exc}')
    finally:
        executor.shutdown()
    return list(review_list)


def get_imdb_data_from_db():
    """
    To retreive the data from mongo db
    :return: list of imdb ids and title
    """
    return Database().retrieve_data('imdb_id')


def perform_scrapping():
    """
    Method for initiating web scrapping.
    This will get the imdb ids and title stored in mongo db
    and uses ids to call fetch_reviews multiprocessing method
    """

    db_ids = get_imdb_data_from_db()

    ids = []
    for pairs in db_ids:
        ids.append(pairs.get('title') + '|' + pairs.get('id'))
    reviews = fetch_reviews(ids)

    Database().store_data_with_list_of_list('raw_reviews', reviews)

    print(f'Finished scrapping and stored ')
    config.logger.info(f'Finished scrapping and stored ')


def store_imdb_ids(movie_series_dict_list):
    """
    This method will go to all the url provided in the params
    and gets the title and imdb ids.  Atlast storing the data
    in mongo db

    :param movie_series_dict_list:
    """
    all_ids = MyDictionary()
    for movie_series_dict in movie_series_dict_list:
        for rated_type, url in movie_series_dict.items():
            obj = Review(url)
            if 'top' in rated_type:
                obj.load_tags('top')
            else:
                obj.load_tags('bottom')

            ids = obj.get_distinct_imdb_ids()
            for titles in ids:
                all_ids.add(titles.split('|')[0], titles.split('|')[1])
            print(f'Finished scrapping imdb ids - {rated_type}')
            wait(2)

    modified_dict_list = []
    for key, value in all_ids.items():
        modified_dict_list.append({'id': key, 'title': value})
    Database().store_data('imdb_id', modified_dict_list)
