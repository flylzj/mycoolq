# coding: utf-8
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from config import BIG_FINGER_GROUP_ID


@nonebot.scheduler.scheduled_job('cron', second='1-59/1')
async def _():
    bot = nonebot.get_bot()
    try:
        await bot.send_group_msg(group_id=BIG_FINGER_GROUP_ID, message="记得点赞")
    except CQHttpError as e:
        print(e)
