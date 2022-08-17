# coding: utf-8
from pydantic import BaseSettings


class Config(BaseSettings):
    setu_token = ""

    class Config:
        extra = "ignore"