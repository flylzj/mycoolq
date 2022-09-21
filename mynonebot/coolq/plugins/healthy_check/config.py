# coding: utf-8
from pydantic import BaseSettings


class Config(BaseSettings):
    ftqq_send_key = ""
    heakthy_check_msg_recipient_id = ""

    class Config:
        extra = "ignore"