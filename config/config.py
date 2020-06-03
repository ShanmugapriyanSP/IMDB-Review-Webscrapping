SERIES_HOME_URL = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"

MOVIES_HOME_URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.61 Safari/537.36'}

REVIEW_URL = 'https://www.imdb.com/title/{id}/reviews?ref_=tt_urv'

MONGO_DB_CLIENT = "mongodb://localhost:27017/"

LOG_FILENAME = "./logs/application.log"

import logging

# Create and configure logger
logging.basicConfig(filename=LOG_FILENAME,
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
