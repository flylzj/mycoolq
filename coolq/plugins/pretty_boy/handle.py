from nonebot import on_command
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot
from nonebot.adapters.cqhttp import GroupMessageEvent
from nonebot import require
from nonebot.log import logger

from .pick_boy_utils import get_today_pretty_boy, base
from .config import CustomConfig

scheduler = require("nonebot_plugin_apscheduler").scheduler
pretty = on_command("靓仔", aliases={'今日靓仔', 'lz'}, priority=5)


@scheduler.scheduled_job("cron", hour="0", minute='0')
async def handle_first_receive():
    logger.info("start handle_first_receive")
    await base(group_id=CustomConfig.group_id, bot_id=CustomConfig.bot_id)


@pretty.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: T_State):
    sex, user_id = get_today_pretty_boy()
    message = f'今日{sex}是 ' + Message(f'[CQ:at,qq={user_id}]')
    await pretty.send(message)
