# coding: utf-8
from nonebot import on_command, CommandSession, scheduler, get_bot
from coolq.db import count_toady_roll, insert_point, count_roll, count_my_roll
import time
from mynonebot.config import MANAGING_GROUPS
from coolq.util.coolq import get_group_user_name
from coolq.plugins.roll.roll import RollEvent


'''
2021.4.9
增加新功能
1.天选之人
每天只有一个人会触发天选之人事件，其得到的点数将为*正*且是点数的*三倍*

2.双倍时刻
每天固定/随机一个时间段，得到的点数为双倍（负数也会双倍）

3.勤劳之人
每天第一个肉必定为正且倍数双倍

4.管理buff
管理员生成的点数+6

'''


@on_command('roll', aliases=('肉', ), only_to_me=False)
async def roll_command(session: CommandSession):
    user_id = session.ctx.get('user_id')
    group_id = session.ctx.get('group_id') if session.ctx.get('group_id') else 0
    count = count_toady_roll(group_id=group_id, user_id=user_id)
    if (group_id in MANAGING_GROUPS and count <= 1) or group_id not in MANAGING_GROUPS:
        roll_event = RollEvent(user_id, group_id)
        roll = roll_event.get_roll()
        message = roll_event.get_roll_message()
        insert_point(group_id=group_id, user_id=user_id, point=roll, roll_time=int(time.time()), message=message)
        await session.send(message=message)
    # else:
    #     await session.send(message='一天只能肉一次哦~')


@on_command('rollcount', aliases=('肉统计', ), only_to_me=False)
async def roll_count_command(session: CommandSession):
    group_id = session.ctx.get('group_id') if session.ctx.get('group_id') else 0
    most_point_user, most_point, most_times_user, most_times = count_roll(group_id)
    message = ""
    if not most_point_user:
        message += "本群暂无点数之王\n"
    else:
        name = await get_group_user_name(group_id, most_point_user)
        message += f"本群点数之王:{name}\n已掷骰子点数总和:{most_point}\n"
    if not most_times_user:
        message += "本群暂无次数之王\n"
    else:
        name = await get_group_user_name(group_id, most_times_user)
        message += f"本群次数之王:{name}\n已掷骰子次数:{most_times}\n"
    await session.send(message=message)


@on_command('myroll', aliases=("我的肉", ), only_to_me=False)
async def my_roll(session: CommandSession):
    group_id = session.ctx.get('group_id') if session.ctx.get('group_id') else 0
    user_id = session.ctx.get("user_id") if session.ctx.get("user_id") else 0

    sum_point = count_my_roll(group_id, user_id)

    message = "你在本群的点数为{}".format(sum_point)

    await session.send(message=message)


@on_command('roll_battle', aliases=("肉拜骰", ), only_to_me=False)
async def roll_battle(session: CommandSession):
    await session.send("battle事件开始，接下来一分钟 内肉所得将被点数最高者们平分")


@scheduler.scheduled_job('cron', **RollEvent.DOUBLE_ROLL_TIME_CRON)
async def double_roll_notice():
    bot = get_bot()
    message = "双倍肉时刻开启，此时肉出的点数将翻倍"
    for group in MANAGING_GROUPS:
        await bot.send_group_msg(group_id=group, message=message)