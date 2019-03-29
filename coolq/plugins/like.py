# coding: utf-8
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from config import LIKED_ID
from nonebot.log import logger


@nonebot.scheduler.scheduled_job('cron', hour="19")
async def _():
    bot = nonebot.get_bot()
    try:
        for id_ in LIKED_ID:
            await bot.send_like(user_id=id_, times=10)
    except CQHttpError as e:
        logger.error(e, exc_info=True)