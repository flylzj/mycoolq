# coding: utf-8
import nonebot
from nonebot import on_command, CommandSession
from coolq.db.model.notice import has_signed_today, sign as sign_to_db
from coolq.util.coolq import at_someone
from config import NEED_SIGN_USER


@on_command("signed", aliases=("打了", ), only_to_me=True)
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
    await session.finish(message=message)


@nonebot.scheduler.scheduled_job('cron', hour="8,17,18,21", minute="*")
async def notice_sign():
    for user_id, group_id in NEED_SIGN_USER.items():
        if not has_signed_today(user_id):
            bot = nonebot.get_bot()
            message = at_someone(user_id) + "打卡"
            await bot.send_group_msg(group_id=group_id, message=message)