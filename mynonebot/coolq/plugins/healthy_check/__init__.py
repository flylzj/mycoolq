# coding: utf-8
from nonebot import require, on_command, get_driver, get_bot
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from nonebot.adapters import Message, Bot, Event
from nonebot.typing import T_State
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.log import logger
from datetime import datetime

from coolq.util.coolq import send_private_message
from coolq.util.ftqq import send_msg_by_wecomchan
from .config import Config


global_config = get_driver().config
plugin_config = Config(**global_config.dict())
scheduler = require("nonebot_plugin_apscheduler").scheduler


status_template_msg = "帐号状态：{}\n" \
                      "接收消息：{}条\n" \
                      "发送消息：{}条\n" \
                      "掉线次数：{}次\n" \
                      "最后一条消息时间：{}" \

def check_status(status):
    is_online = status.get("online")
    stat = status.get("stat")
    if is_online:
        is_online = "在线"
        last_message_time = stat.get('last_message_time')
        if not last_message_time:
            last_message_time = "无"
        else:
            last_message_time = datetime.fromtimestamp(last_message_time).strftime("%Y-%m-%d %H:%M:%S")
    return is_online, status_template_msg.format(
        is_online, 
        stat.get("message_received"),
        stat.get("message_sent"),
        stat.get("lost_times"),
        last_message_time
    )

@scheduler.scheduled_job("cron", hour="12")
async def check_gocqhttp():
    bot = get_bot()
    status = await bot.get_status()  # call /get_status
    logger.info("status:" + str(status))
    is_online, status_msg = check_status(status)
    if not is_online:
        await send_msg_by_wecomchan(key=plugin_config.wecom_send_key, msg=status_msg)
    else:
        await send_private_message(plugin_config.heakthy_check_msg_recipient_id, status_msg)


get_status_command = on_command("status")

@get_status_command.handle()
async def sign_command_handle(bot: Bot, event: Event, state: T_State):
    status = await bot.get_status()  # call /get_status
    logger.info("status:" + str(status))
    _, status_msg = check_status(status)
    await get_status_command.finish(status_msg)