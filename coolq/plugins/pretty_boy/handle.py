from nonebot import on_command
import nonebot
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot
from nonebot.adapters.cqhttp import GroupMessageEvent
from nonebot import require
from nonebot.log import logger

from .pick_boy import check_boy
from . import config


async def base(group_id, bot_id):
    bot: Bot = nonebot.get_bots()[bot_id]
    boys = await bot.call_api('get_group_member_list', **{'group_id': group_id})
    sex, user_id = check_boy(boys=boys)
    logger.info(f"the boy {user_id}")
    message = config.message + Message(f'[CQ:at,qq={user_id}]')
    return await bot.call_api('send_group_msg', **{
        'group_id': group_id,
        'message': message
    })


scheduler = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job("cron", hour="07", minute='52')
async def handle_first_receive():
    # await base(group_id=config.group_id,bot_id=config.bot_id)
    logger.info("start handle_first_receive")
    await base(group_id=config.group_id, bot_id=config.bot_id)

pretty = on_command("靓仔", aliases={'今日靓仔', 'lz'}, priority=5)


@pretty.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: T_State):
    message = f'今日{config.the_boy_sex}是 ' + Message(f'[CQ:at,qq={config.user_id}]')
    await pretty.send(message)