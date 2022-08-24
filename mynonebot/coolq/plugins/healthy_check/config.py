# coding: utf-8
from pydantic import BaseSettings


class Config(BaseSettings):
    zerotier_controller_url = ""
    zerotier_user = ""
    zerotier_password = ""

    class Config:
        extra = "ignore"