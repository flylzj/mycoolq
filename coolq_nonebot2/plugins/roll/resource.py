# coding: utf-8
import random
import time
from .models import RollHistory, RollEvent, RollEventEnum


class RollResource(object):
    ROLL_MANAGER_USERS = (
        1449902124,
        2188840643
    )

    DOUBLE_ROLL_TIME_CRON = {
        "hour": "12"
    }
    DOUBLE_ROLL_TIME = 12
    GOD_SELECTED_PROB = 50

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id
        self.roll = 0
        self.roll_id = 0

    def gen_roll(self):
        self.roll = random.randint(-6, 6)
        self.roll_id = RollHistory.insert_point(
            group_id=self.group_id,
            user_id=self.user_id,
            point=self.roll,
            roll_time=int(time.time()),
            message=""
        )

    def __is_god_selected(self):
        return 1 == random.randint(1, self.GOD_SELECTED_PROB)
