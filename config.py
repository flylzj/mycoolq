# coding: utf-8
from nonebot.default_config import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# db
ENGINE = create_engine('sqlite:///./data/data.db')

SESSION = sessionmaker(bind=ENGINE)
###


SUPERUSERS = {1449902124}

BIG_FINGER_GROUP_ID = 654137970

MOVIE_URL = "http://www.coupling.pw"

# 和风天气api
HWEATHER_KEY = 'a735882b1acc478eb52c9bd5926d6bc4'
HWEATHER_API = 'https://free-api.heweather.net/s6/weather/{}'
WEATHER_TYPE = {
    '实况天气': 'now',
    '3-10天预报': 'forecast',
    '逐小时预报': 'hourly',
    '生活指数': 'lifestyle'
}

WEATHER_CONFIG = {
    1449902124: "新建,南昌",
    2864158129: "滨湖,无锡"
}

# REDIS_CONFIG = {
#     "host": "redis",
#     "decode_responses": True
# }
#
# POOL = ConnectionPool(**REDIS_CONFIG)