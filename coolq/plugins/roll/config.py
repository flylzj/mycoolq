# coding: utf-8
from pydantic import BaseSettings


class Config(BaseSettings):
    DOUBLE_ROLL_TIME_CRON = {
        "hour": "12"
    }

    MANAGING_GROUPS = [855508068, 97795387]

    class Config:
        extra = "ignore"
