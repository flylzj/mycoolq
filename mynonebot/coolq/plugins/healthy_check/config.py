# coding: utf-8
from pydantic import BaseSettings


class Config(BaseSettings):
    ftqq_send_key = ""
    wecom_send_key = ""
    wecom_push_url = ""
    heakthy_check_msg_recipient_id = ""

    class Config:
        extra = "ignore"