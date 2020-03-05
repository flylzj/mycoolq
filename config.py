# coding: utf-8
from nonebot.default_config import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# db
ENGINE = create_engine('sqlite:///./data/data.db')

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

QQ_GROUP_CAPTCHA_HINT_IMG = "https://flythief.cn/qq-group-captcha-hint.png"

## python lib helper

LIB_URL = "https://docs.python.org/zh-cn/3.8/library/index.html"

LIB_ROOT_URL = "https://docs.python.org/zh-cn/3.8/library/"

LOCAL_LIB_ROOT_URL = "https://coolq.flythief.cn/python-docs/index.html"

LANG_REF_ROOT_URL = "https://docs.python.org/zh-cn/3/reference/index.html"

LOCAL_LANG_REF_ROOT_URL = "http://114.55.252.170:8081/python-docs/reference/index.html"

THIRD_LIB_ROOT_URL = "https://pypi.org/project/"

PYTHON_TUTORIALS_URL = "https://flythief.cn/post/python-tutorials/"

MOVIE_URL = "http://www.coupling.pw"

COMMAND_START = {'', '/'}

# REDIS_CONFIG = {
#     "host": "redis",
#     "decode_responses": True
# }
#
# POOL = ConnectionPool(**REDIS_CONFIG)