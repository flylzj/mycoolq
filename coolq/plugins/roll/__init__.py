# coding: utf-8
from nonebot import on_command, CommandSession
from random import randint
from coolq.db.model.roll import count_toady_roll, insert_point, count_roll
import time
from config import MANAGING_GROUPS


@on_command('roll', aliases=('肉', ), only_to_me=False)
async def roll_command(session: CommandSession):
    group_id = session.ctx.get('group_id') if session.ctx.get('group_id') else 0
    user_id = session.ctx.get('user_id')
    count = count_toady_roll(group_id=group_id, user_id=user_id)
    if count < 3 or group_id not in MANAGING_GROUPS:
        roll = randint(-6, 6)
        message = "你肉到了{}点"
        insert_point(group_id=group_id, user_id=user_id, point=roll, roll_time=int(time.time()))
        await session.send(message=message.format(roll))


@on_command('rollcount', aliases=('肉统计', ), only_to_me=False)
async def roll_count_command(session: CommandSession):
    group_id = session.ctx.get('group_id') if session.ctx.get('group_id') else 0
    message = count_roll(group_id)
    await session.send(message=message)