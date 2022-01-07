# coding: utf-8
from nonebot import get_driver, require, on_command
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from coolq.util.coolq import send_message
from .config import Config
from .sign_util import T00lsSign

scheduler = require("nonebot_plugin_apscheduler").scheduler

global_config = get_driver().config

plugin_config = Config(**global_config.dict())


class SignBox:

    @staticmethod
    async def t00ls_sign():
        username = plugin_config.t00ls_username
        login_form = {
            'action': 'login',
            'username': username,
            'password': plugin_config.t00ls_password,
            'questionid': plugin_config.t00ls_questionid,
            'answer': plugin_config.t00ls_answer
        }
        t00ls = T00lsSign(username, login_form)

        return await t00ls.sign_and_get_profile()


# @scheduler.scheduled_job("cron", second="*/10") # debug
@scheduler.scheduled_job("cron", hour="8")
async def t00ls_sign_cron():
    await send_message(message_type="private", recipient_id="1449902124", message=SignBox.t00ls_sign())


sign_command = on_command("sign", aliases={"签到"}, permission=SUPERUSER)


@sign_command.handle()
async def sign_command_handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if not args:
        pass
    elif args == "土司":
        await sign_command.finish(await SignBox.t00ls_sign())


