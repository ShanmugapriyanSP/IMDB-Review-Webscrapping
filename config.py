"""
Constants and config properties will be available here
"""

import logging
import os

SERIES_TOP_URL = 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'
MOVIES_TOP_URL = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
SERIES_BOTTOM_URL = 'https://www.imdb.com/list/ls063837343/?sort=list_order' \
                    ',asc&st_dt=&mode=simple&page=1&ref_=ttls_vw_smp'
MOVIES_BOTTOM_URL = 'https://www.imdb.com/list/ls031780759/?sort=list_order,' \
                    'asc&st_dt=&mode=simple&page=1&ref_=ttls_vw_smp'

GOOD_REVIEW_URL = 'https://www.imdb.com/title/{id}/reviews?ref_=tt_urv'
BAD_REVIEW_URL = 'https://www.imdb.com/title/{id}/reviews?sort=userRating&dir=asc&ratingFilter=0'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 '
                  '(Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.61 Safari/537.36'}

MONGO_DB_CLIENT = "mongodb://localhost:27017/"
SCHEMA_NAME = 'reviews'


# 90% Cpu Utilization
MAX_WORKERS = int(os.cpu_count() // 1.10)

LOG_FILENAME = "logs/application.log"
# Create and configure logger
logging.basicConfig(filename=LOG_FILENAME,
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
