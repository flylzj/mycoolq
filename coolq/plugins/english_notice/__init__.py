# coding: utf-8
import nonebot
from  coolq.db.model.english_record import get_recorded_today
from aiocqhttp.exceptions import Error as CQHttpError
from config import BIG_FINGER_GROUP_ID, ENGLISH_USERS
from nonebot.log import logger


# @nonebot.scheduler.scheduled_job('cron', hour="*", minute='*', second="1-59/30")
# @nonebot.scheduler.scheduled_job('cron', hour="0", minute='0')
# async def _():
#     bot = nonebot.get_bot()
#
#     text = "阿向！这是刘崽给你准备的礼物，希望你能喜欢，生日快乐~\nhttps://www.bilibili.com/video/av70857887"
#     await bot.send_private_msg(user_id=1449902124, message=text)
#     await bot.send_group_msg(group_id=BIG_FINGER_GROUP_ID, message=text)
    # try:
    #     records = get_recorded_today()
    #     recorded_users = [int(record.user_id) for record in records]
    #     for user in ENGLISH_USERS:
    #         if user not in recorded_users:
    #             # await bot.send_group_msg(group_id=BIG_FINGER_GROUP_ID, message="今天背单词了吗")
    #             msg = "今天还没有背单词~" + "[CQ:at,qq={}]".format(user)
    #             await bot.send_group_msg(group_id=BIG_FINGER_GROUP_ID, message=msg)
    # except CQHttpError as e:
    #     logger.error(e, exc_info=True)