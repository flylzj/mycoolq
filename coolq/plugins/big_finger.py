# coding: utf-8
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from config import BIG_FINGER_GROUP_ID


@nonebot.scheduler.scheduled_job('interval', hours="8, 21")
async def _():
    bot = nonebot.get_bot()
    try:
        await bot.send_group_msg(group_id=BIG_FINGER_GROUP_ID, message="为了大拇指，记得去ta点赞")
    except CQHttpError as e:
        print(e)
