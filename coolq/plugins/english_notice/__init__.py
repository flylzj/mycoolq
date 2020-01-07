# coding: utf-8
import nonebot
from config import BIG_FINGER_GROUP_ID


@nonebot.scheduler.scheduled_job('cron', hour="5", minute='30')
async def _():
    bot = nonebot.get_bot()
    text = "记得带学生证身份证充电器啊啊啊～"
    # await bot.send_private_msg(user_id=1449902124, message=text)
    await bot.send_group_msg(group_id=BIG_FINGER_GROUP_ID, message=text)