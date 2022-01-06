# coding: utf-8
from pydantic import BaseSettings


class Config(BaseSettings):
    hass_host = ""
    hass_token = ""

    class Config:
        extra = "ignore"