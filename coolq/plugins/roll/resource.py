# coding: utf-8
import random
from datetime import datetime
import time
from nonebot.log import logger
from coolq.db.models import RollHistory, RollEvent, RollEventEnum
from coolq.util.coolq import get_coolq_bot


class RollResource(object):
    # MAX_ROLL_COUNT_ONE_DAY = 1
    # for test
    MAX_ROLL_COUNT_ONE_DAY = 1000

    ROLL_MANAGER_USERS = (
        "1449902124",
        "2188840643",
        "732599980"
    )

    DOUBLE_ROLL_TIME = 12
    GOD_SELECTED_PROB = 50
    ROLL_RANGE = (-6, 6)

    def __init__(self, event, bot):
        event_data = event.dict()
        logger.info("event data {}".format(event_data))
        user_id = event.get_user_id()
        group_id = event_data.get("group_id") if event_data.get("group_id") else 0
        self.bot = bot
        self.user_id = user_id
        self.group_id = group_id

    def gen_roll(self):
        roll = random.randint(*self.ROLL_RANGE)
        return roll

    def insert_roll(self, roll):
        roll_id = RollHistory.insert_point(
            group_id=self.group_id,
            user_id=self.user_id,
            point=roll,
            roll_time=int(time.time()),
            message=""
        )
        return roll_id

    def __is_god_selected(self):
        return 1 == random.randint(1, self.GOD_SELECTED_PROB)

    def can_roll_today(self):
        return RollHistory.count_toady_roll(user_id=self.user_id, group_id=self.group_id) < self.MAX_ROLL_COUNT_ONE_DAY

    def roll_with_event(self):
        roll = self.gen_roll()
        message = "你肉到了{}点".format(roll)
        roll_id = self.insert_roll(roll)
        if roll_id == 0:
            return 0, "肉失败了"

        now = int(time.time())
        # 天选之人
        event_info = {
            "roll_id": roll_id,
            "group_id": self.group_id,
            "user_id": self.user_id,
        }
        if self.__is_god_selected() and not RollEvent.has_god_select_man_today(self.group_id):
            event_info["event_type"] = RollEventEnum.god_select_event.int_value
            event_info["event_time"] = now
            event_id = RollEvent.insert_event(**event_info)
            if event_id != 0:
                roll = abs(roll) * 3
                message += "\n恭喜你触发天选之人，点数转正并*3"

        # 双倍时刻
        if datetime.now().time().hour == self.DOUBLE_ROLL_TIME:
            event_info["event_type"] = RollEventEnum.double_event.int_value
            event_info["event_time"] = now
            event_id = RollEvent.insert_event(**event_info)
            if event_id != 0:
                roll *= 2
                message += "\n恭喜你触发双倍时刻，点数*2"

        # 勤劳之人
        if not RollEvent.has_first_man_today(self.group_id):
            event_info["event_type"] = RollEventEnum.first_man_event.int_value
            event_info["event_time"] = now
            event_id = RollEvent.insert_event(**event_info)
            if event_id != 0:
                roll = abs(roll) * 2
                message += "\n恭喜你触发勤劳之人，点数转正*2"

        # 管理buff
        if self.user_id in self.ROLL_MANAGER_USERS:
            event_info["event_type"] = RollEventEnum.manager_event.int_value
            event_info["event_time"] = now
            event_id = RollEvent.insert_event(**event_info)
            if event_id != 0:
                if random.randint(0, 1):
                    roll += 6
                    message += "\n恭喜你触发管理buff，点数+6"
                else:
                    roll -= 6
                    message += "\n恭喜你触发管理debuff，点数-6"
        message += "\n最终点数为{}".format(roll)
        RollHistory.update_roll(roll_id, roll, message)
        return roll, message

    def my_roll(self):
        roll_point = RollHistory.count_my_roll(group_id=self.group_id, user_id=self.user_id)
        message = "你在本群的点数为{}".format(roll_point)
        return message

    async def roll_count(self):
        message = "本群点数之王:{}\n已掷骰子点数总和:{}\n本群次数之王:{}\n已掷骰子次数:{}"
        most_point_user, most_point, most_times_user, most_times = RollHistory.count_roll(self.group_id)
        coolq_bot = get_coolq_bot()
        if coolq_bot:
            if self.group_id != 0 and most_point_user != 0:
                most_point_user = await coolq_bot.get_group_user_nickname(self.group_id, most_point_user)
            else:
                most_point_user = ""

            if self.group_id != 0 and most_times_user != 0:
                most_times_user = await coolq_bot.get_group_user_nickname(self.group_id, most_times_user)
            else:
                most_times_user = ""
        return message.format(
            most_point_user,
            most_point,
            most_times_user,
            most_times
        )





