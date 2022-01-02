# coding: utf-8
from pydantic import BaseSettings


class Config(BaseSettings):
    MANAGING_GROUPS: list = ["855508068", "97795387"]

    class Config:
        extra = "ignore"