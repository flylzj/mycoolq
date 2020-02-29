# coding: utf-8
from nonebot.default_config import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# db
ENGINE = create_engine('sqlite:///./data/data.db', echo=True)

SESSION = sessionmaker(bind=ENGINE)
###

## english

SUPERUSERS = {1449902124}

## remover manager
MANAGING_GROUPS = [
    855508068,
    97795387,
    654137970
]

MOVIE_URL = "http://www.coupling.pw"

COMMAND_START = {'', '/'}

# REDIS_CONFIG = {
#     "host": "redis",
#     "decode_responses": True
# }
#
# POOL = ConnectionPool(**REDIS_CONFIG)