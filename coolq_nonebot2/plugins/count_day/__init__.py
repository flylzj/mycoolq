# coding: utf-8
import nonebot
from nonebot import on_command
from nonebot import require
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from coolq_nonebot2.util.coolq import CoolqBot
from .resource import to_zero, increase_one, get_need_increase


count_day = on_command("count_day", aliases={"计数", })


@count_day.handle()
async def count_day_command(bot: Bot, event: Event, state: T_State):
    user_id = event.get_user_id()
    res = to_zero(user_id)
    if res:
        await bot.send(event, "重新开始计数")
    else:
        await bot.send(event, message='开始计数')


scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job('cron', hour="23")
async def increase_day():
    bot = CoolqBot()
    if bot.bot:
        for d in get_need_increase():
            user_id = d.user_id
            increase_one(user_id)
            message = f"{d.days}天"
            await bot.send_private_message(message, user_id)