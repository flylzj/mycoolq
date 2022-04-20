# coding: utf-8
from nonebot import get_driver, require, on_command
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.log import logger

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
    message = await SignBox.t00ls_sign()
    await send_message(message_type="private", recipient_id="1449902124", message=message)


# @scheduler.scheduled_job("cron", hour="21", minute="40")
# async def notice_class():
#    await send_message(message_type="private", recipient_id="1401924203", message="下课啦！下课啦！下课啦")


# @scheduler.scheduled_job("cron", hour="5", minute="25")
# async def notice_morning():                                   
#     await send_message(message_type="private", recipient_id="1401924203", message="早安")


sign_command = on_command("t00ls_sign")

@sign_command.handle()
async def sign_command_handle(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if not plain_text:
        pass
    elif plain_text == "土司":
        message = await SignBox.t00ls_sign()
        logger.debug("message", message)
        await sign_command.finish(message)


