# coding: utf-8
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from config import BIG_FINGER_GROUP_ID
from nonebot.log import logger
import redis


@nonebot.scheduler.scheduled_job('cron', hour="22, 23", minute='30')
async def _():
    bot = nonebot.get_bot()
    try:
        await bot.send_group_msg(group_id=BIG_FINGER_GROUP_ID, message="今天背单词了吗")
    except CQHttpError as e:
        logger.error(e, exc_info=True)