"""
Application for web scrapping movie and series reviews(raw data) from
IMDB website.

Data to be used for Sentiment analysis, Recommendation, Genre prediction
"""
from concurrent.futures import ProcessPoolExecutor as Pool
from datetime import datetime

import config
from movie_review_webscrapping.main import perform_scrapping

if __name__ == '__main__':
    START_TIME = datetime.now()
    MOVIE_SERIES_LIST = [{'movies_top': config.MOVIES_TOP_URL},
                         {'series_top': config.SERIES_TOP_URL},
                         {'movies_bottom': config.MOVIES_BOTTOM_URL},
                         {'series_bottom': config.SERIES_BOTTOM_URL}
                         ]
    try:
        with Pool(max_workers=config.MAX_WORKERS) as executor:
            executor.map(perform_scrapping, MOVIE_SERIES_LIST)
    except Exception as exception:
        config.logger.error(f'Exception occurred in perform_scrapping method - {exception}')
    finally:
        executor.shutdown()

    FINISH_TIME = datetime.now()

    print(FINISH_TIME - START_TIME)
