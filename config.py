"""
Constants and config properties for the the
application will be available here
"""

import logging
import os

SERIES_TOP_URL = 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'
MOVIES_TOP_URL = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
SERIES_BOTTOM_URL = 'https://www.imdb.com/list/ls063837343/?sort=list_order' \
                    ',asc&st_dt=&mode=simple&page=1&ref_=ttls_vw_smp'
MOVIES_BOTTOM_URL = 'https://www.imdb.com/list/ls031780759/?sort=list_order,' \
                    'asc&st_dt=&mode=simple&page=1&ref_=ttls_vw_smp'

GENRE_URL_PAGE1 = 'https://www.imdb.com/search/title/?genres={GENRE_TYPE}&explore' \
                  '=title_type,genres&view=simple'
GENRE_URL_PAGE2 = 'https://www.imdb.com/search/title/?genres={GENRE_TYPE}&view=' \
                  'simple&start=51&explore=title_type,genres&ref_=adv_nxt'
GENRE_URL_PAGE3 = 'https://www.imdb.com/search/title/?genres={GENRE_TYPE}&view=' \
                  'simple&start=101&explore=title_type,genres&ref_=adv_nxt'
GENRE_URL_PAGE4 = 'https://www.imdb.com/search/title/?genres={GENRE_TYPE}&view=' \
                  'simple&start=151&explore=title_type,genres&ref_=adv_nxt'
GENRE_URL_PAGE5 = 'https://www.imdb.com/search/title/?genres={GENRE_TYPE}&view=' \
                  'simple&start=201&explore=title_type,genres&ref_=adv_nxt'

GOOD_REVIEW_URL = 'https://www.imdb.com/title/{id}/reviews?ref_=tt_urv'
BAD_REVIEW_URL = 'https://www.imdb.com/title/{id}/reviews?sort=userRating&dir=asc&ratingFilter=0'

GENRE_LIST = ['comedy',
              'sci-fi',
              'horror',
              'romance',
              'action',
              'thriller',
              'drama',
              'mystery',
              'crime',
              'animation',
              'adventure',
              'fantasy',
              'comedy,romance',
              'action,comedy',
              'superhero'
              ]

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

# For anonymous scrapping
# SOCKS_PORT = 7000  # You can change the port number
#
# tor_process = stem.process.launch_tor_with_config(
#     tor_cmd='C:\\Users\\Bala\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe',
#     config={
#         'SocksPort': str(SOCKS_PORT),
#     },
# )
#
# socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5,
#                       addr="127.0.0.1",
#                       port=SOCKS_PORT)
# socket.socket = socks.socksocket
