from datetime import datetime

from config import config
from movie_review_webscrapping import main

if __name__ == '__main__':
    START_TIME = datetime.now()
    MOVIE_SERIES_LIST = [{'movies_top': config.MOVIES_TOP_URL},
                         {'series_top': config.SERIES_TOP_URL},
                         {'movies_bottom': config.MOVIES_BOTTOM_URL},
                         {'series_bottom': config.SERIES_BOTTOM_URL}]
    main.start(MOVIE_SERIES_LIST)
    FINISH_TIME = datetime.now()

    print(FINISH_TIME - START_TIME)
