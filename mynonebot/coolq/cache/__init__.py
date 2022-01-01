# coding: utf-8
import redis
from mynonebot.config import REDIS_CONFIG

POOL = redis.ConnectionPool(**REDIS_CONFIG)


def get_conn() -> redis.Redis:
    return redis.Redis(connection_pool=POOL)

