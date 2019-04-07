# coding: utf-8
from nonebot.default_config import *
from redis import ConnectionPool


SUPERUSERS = {1449902124}

BIG_FINGER_GROUP_ID = 654137970

LIKED_ID = (2864158129, 1449902124)

REDIS_CONFIG = {
    "host": "redis",
    "decode_response": True
}

POOL = ConnectionPool(**REDIS_CONFIG)