# coding: utf-8
import nonebot
from nonebot import on_command, CommandSession
from coolq.db.model.notice import has_signed_today, sign as sign_to_db
from coolq.util.coolq import at_someone
from config import  NEED_SIGN_USER


@on_command("signed", aliases="打了")
async def sign(session: CommandSession):
    user_id = session.ctx.get('user_id')
    message = at_someone(user_id)
    if not has_signed_today(user_id):
        if sign_to_db(user_id):
            message += "打卡成功"
        else:
            message += "打卡失败"
    else:
        message += "已经打过卡了"
    await session.bot.send_group_msg(group_id=NEED_SIGN_USER.get(user_id), message=message)


@nonebot.scheduler.scheduled_job('cron', hour="8,17,21", minute="*")
async def notice_sign():
    for group_id, user_id in NEED_SIGN_USER:
        if not has_signed_today(user_id):
            bot = nonebot.get_bot()
            message = at_someone(user_id)
            await bot.send_group_msg(group_id=group_id, message=message)