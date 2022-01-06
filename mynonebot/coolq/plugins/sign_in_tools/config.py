# coding: utf-8
from pydantic import BaseSettings


class Config(BaseSettings):
    t00ls_username = ""
    t00ls_password = ""
    t00ls_questionid = ""
    t00ls_answer = ""

    class Config:
        extra = "ignore"