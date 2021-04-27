# coding: utf-8
from nonebot import require
from coolq.util.coolq import get_coolq_bot

scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job('cron', hour="21", minute="1-59/10")
async def notice():
    group_id = 1076038734
    user_ids = [
        "1449902124",
        "646503792"
    ]
    bot = get_coolq_bot()
    if bot:
        for user_id in user_ids:
            message = f"[CQ:at,qq={user_id}]"
            await bot.send_group_msg(group_id=group_id, message=message)