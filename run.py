"""
Application for web scrapping movie and series reviews(raw data) from
IMDB website and storing it in Mongo DB

Data to be used for Sentiment analysis, Recommendation, Genre prediction
"""
from datetime import datetime

import config
from movie_review_webscrapping.main import perform_scrapping, store_imdb_ids


def prepare_dynamic_urls():
    url_dict_list = [{'movies_top': config.MOVIES_TOP_URL},
                     {'series_top': config.SERIES_TOP_URL},
                     {'movies_bottom': config.MOVIES_BOTTOM_URL},
                     {'series_bottom': config.SERIES_BOTTOM_URL}
                     ]

    for genre in config.GENRE_LIST:
        url_dict_list.append(
            {'bottom_' + genre + '_page1': config.GENRE_URL_PAGE1.replace("{GENRE_TYPE}", genre)})
        url_dict_list.append(
            {'bottom_' + genre + '_page2': config.GENRE_URL_PAGE1.replace("{GENRE_TYPE}", genre)})
        url_dict_list.append(
            {'bottom_' + genre + '_page3': config.GENRE_URL_PAGE1.replace("{GENRE_TYPE}", genre)})
        url_dict_list.append(
            {'bottom_' + genre + '_page4': config.GENRE_URL_PAGE1.replace("{GENRE_TYPE}", genre)})
        url_dict_list.append(
            {'bottom_' + genre + '_page5': config.GENRE_URL_PAGE1.replace("{GENRE_TYPE}", genre)})

    return url_dict_list


if __name__ == '__main__':
    START_TIME = datetime.now()
    MOVIE_SERIES_LIST = prepare_dynamic_urls()

    # Below code is commented because multiprocessing causing too
    # many requests to IMDB site and making it down similar to DDOS attack

    # try:
    #     with Pool(max_workers=config.MAX_WORKERS) as executor:
    #         executor.map(perform_scrapping, MOVIE_SERIES_LIST)
    # except Exception as exception:
    #     config.logger.error(f'Exception occurred in perform_scrapping method - {exception}')
    # finally:
    #     executor.shutdown()

    store_imdb_ids(MOVIE_SERIES_LIST)

    perform_scrapping()

    FINISH_TIME = datetime.now()

    print(FINISH_TIME - START_TIME)
