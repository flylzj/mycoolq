# coding: utf-8
from nonebot import on_command, CommandSession, scheduler, get_bot
from random import randint
from coolq.db.model.roll import count_toady_roll, insert_point, count_roll, count_my_roll
from coolq.cache import get_conn as get_redis_conn
import time
from config import MANAGING_GROUPS
from coolq.util.coolq import get_group_user_name
from datetime import datetime


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


class RollEvent:
    ROLL_MANAGER_USERS = (
        1449902124,
        2188840643
    )

    DOUBLE_ROLL_TIME_CRON = {
        "hour": "12"
    }
    DOUBLE_ROLL_TIME = 12

    REDIS_GOD_SELECTED_MAN_KEY = "roll-god-select-{}-{}-{}"
    REDIS_FIRST_ROLL_MAN_KEY = "roll-first-man-{}-{}-{}"

    GOD_SELECTED_PROB = 50

    def __init__(self, user_id, group_id):
        self.__user_id = user_id
        self.__group_id = group_id
        self.__roll = randint(-6, 6)
        self.__message = "你肉到了{}点"
        self.__handled = False

    def __get_first_man_key(self):
        return self.REDIS_FIRST_ROLL_MAN_KEY.format(
            "group" if self.__group_id != 0 else "user",
            self.__group_id if self.__group_id != 0 else self.__user_id,
            datetime.now().date().strftime("%Y-%m-%d")
        )

    def __has_first_man_today(self):
        key = self.__get_first_man_key()
        r = get_redis_conn()
        return r.get(key)

    def __set_first_man_today(self):
        key = self.__get_first_man_key()
        r = get_redis_conn()
        r.set(key, "1")

    def __is_manager(self):
        return self.__user_id in self.ROLL_MANAGER_USERS

    def __get_god_selected_man_key(self):
        return self.REDIS_GOD_SELECTED_MAN_KEY.format(
            "group" if self.__group_id != 0 else "user",
            self.__group_id if self.__group_id != 0 else self.__user_id,
            datetime.now().date().strftime("%Y-%m-%d")
        )

    def __is_god_selected(self):
        return 1 == randint(1, self.GOD_SELECTED_PROB)

    def __has_god_selected_today(self):
        key = self.__get_god_selected_man_key()
        r = get_redis_conn()
        return r.get(key)

    def __set_god_selected(self):
        key = self.__get_god_selected_man_key()
        r = get_redis_conn()
        r.set(key, "1")

    def _check_manager_event(self):
        if self.__is_manager():
            self.__roll += 6
            self.__message += "\n恭喜你触发了管理员事件，点数加6"
            return True

    def _check_god_selected_event(self):
        # 命中天选且没有天选
        if self.__is_god_selected() and not self.__has_god_selected_today():
            self.__roll = abs(self.__roll) * 3
            self.__set_god_selected()
            self.__message += "\n恭喜你触发了天选之人事件，点数转正并*3"
            return True

    def _check_double_roll_event(self):
        if datetime.now().time().hour == self.DOUBLE_ROLL_TIME:
            self.__roll = self.__roll * 2
            self.__message += "\n触发了双倍时刻事件，点数*3"
            return True

    def _check_first_event(self):
        if not self.__has_first_man_today():
            self.__roll = abs(self.__roll) * 2
            self.__message += "\n恭喜你触发了勤劳之人事件，点数转正并*2"
            return True

    def _handle_roll(self):
        self._check_manager_event()
        self._check_double_roll_event()
        self._check_god_selected_event()
        self.__handled = True

    def get_roll(self):
        if not self.__handled:
            self._handle_roll()
        return self.__roll

    def get_roll_message(self):
        return self.__message.format(self.__roll)


@on_command('roll', aliases=('肉', ), only_to_me=False)
async def roll_command(session: CommandSession):
    user_id = session.ctx.get('user_id')
    group_id = session.ctx.get('group_id') if session.ctx.get('group_id') else 0
    count = count_toady_roll(group_id=group_id, user_id=user_id)
    # if group_id not in MANAGING_GROUPS and count <= 1:
    if count <= 1:
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


@scheduler.scheduled_job('cron', **RollEvent.DOUBLE_ROLL_TIME_CRON)
async def double_roll_notice():
    bot = get_bot()
    message = "双倍肉时刻开启，此时肉出的点数将翻倍"
    for group in MANAGING_GROUPS:
        await bot.send_group_msg(group_id=group, message=message)