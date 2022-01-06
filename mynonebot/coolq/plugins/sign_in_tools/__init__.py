# coding: utf-8
from nonebot import get_driver, require

from coolq.util.coolq import send_message
from .config import Config
from .sign_util import T00lsSign

scheduler = require("nonebot_plugin_apscheduler").scheduler

global_config = get_driver().config

plugin_config = Config(**global_config.dict())


# @scheduler.scheduled_job("cron", second="*/10") # debug
@scheduler.scheduled_job("cron", hour="8")
async def t00ls_sign_cron():
    username = plugin_config.t00ls_username
    login_form = {
        'action': 'login',
        'username': username,
        'password': plugin_config.t00ls_password,
        'questionid': plugin_config.t00ls_questionid,
        'answer': plugin_config.t00ls_answer
    }
    t00ls = T00lsSign(username, login_form)
    status, reason = await t00ls.login_and_sign()

    message = "土司签到完成\nstatus:{}\nreason:{}".format(status, reason)
    await send_message(message_type="private", recipient_id="1449902124", message=message)



