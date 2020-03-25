# coding: utf-8
from nonebot import on_command, CommandSession
from coolq.db.model.count_day import to_zero, increase_one, get_need_increase
import nonebot


@on_command('count_day', aliases=('计数', ), only_to_me=False)
async def count_day_command(session: CommandSession):
    user_id = session.ctx.get('user_id')
    res = to_zero(user_id)
    if res:
        await session.send(message='重新开始计数')
    else:
        await session.send(message='开始计数')


@nonebot.scheduler.scheduled_job('cron', hour="23")
async def increase_day():
    bot = nonebot.get_bot()
    for d in get_need_increase():
        user_id = d.user_id
        increase_one(user_id)
        message = f"{d.days}天"
        try:
            await bot.send_private_message(user_id=user_id, message=message)
        except Exception as e:
            pass