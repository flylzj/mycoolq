# coding: utf-8
from pydantic import BaseSettings


class Config(BaseSettings):

    class Config:
        extra = "ignore"
