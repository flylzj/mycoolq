# coding: utf-8
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from config import BIG_FINGER_GROUP_ID


@nonebot.scheduler.scheduled_job('cron', hour="23", minute="59")
async def _():
    bot = nonebot.get_bot()
    try:
        await bot.send_group_msg(group_id=BIG_FINGER_GROUP_ID, message="不要当熬夜冠军了, 快去睡觉~")
    except CQHttpError as e:
        bot.logger.error(e)
