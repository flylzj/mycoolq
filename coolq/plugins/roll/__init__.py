# coding: utf-8
from nonebot import on_command, CommandSession
from random import randint
from coolq.db.model.roll import count_toady_roll, insert_point, count_roll
import time
from config import MANAGING_GROUPS
from coolq.util.coolq import get_group_user_name


@on_command('roll', aliases=('肉', ), only_to_me=False)
async def roll_command(session: CommandSession):
    group_id = session.ctx.get('group_id') if session.ctx.get('group_id') else 0
    user_id = session.ctx.get('user_id')
    count = count_toady_roll(group_id=group_id, user_id=user_id)
    if count < 1 or group_id not in MANAGING_GROUPS:
        roll = randint(-6, 6)
        message = "你肉到了{}点"
        insert_point(group_id=group_id, user_id=user_id, point=roll, roll_time=int(time.time()))
        await session.send(message=message.format(roll))
    else:
        await session.send(message='一天只能肉一次哦~')


@on_command('rollcount', aliases=('肉统计', ), only_to_me=False)
async def roll_count_command(session: CommandSession):
    group_id = session.ctx.get('group_id') if session.ctx.get('group_id') else 0
    most_point_user, most_point, most_times_user, most_times = count_roll(group_id)
    message = ""
    if not most_point_user:
        message += "本群暂无点数之王\n"
    else:

        message += f"本群点数之王:{await get_group_user_name(group_id, most_point_user)}\n已掷骰子点数总和:{most_point}\n"
    if not most_times_user:
        message += "本群暂无次数之王\n"
    else:
        message += f"本群次数之王:{await get_group_user_name(group_id, most_times_user)}\n已掷骰子次数:{most_times}\n"
    await session.send(message=message)


