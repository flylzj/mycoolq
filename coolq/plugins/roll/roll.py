# coding: utf-8
from random import randint
from coolq.cache import get_conn as get_redis_conn
from nonebot.log import logger
from datetime import datetime


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
        self.__message = "你肉到了{}点".format(self.__roll)
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
        v = r.get(key)
        logger.debug("__get_first_man_key get {} value {}".format(key, v))
        return v

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
        v = r.get(key)
        logger.debug("__get_god_selected_man_key get {} value {}".format(key, v))
        return v

    def __set_god_selected(self):
        key = self.__get_god_selected_man_key()
        r = get_redis_conn()
        r.set(key, "1")

    def _check_manager_event(self):
        if self.__is_manager():
            self.__roll += 6
            self.__message += "\n恭喜你触发了管理员事件，点数加6"

    def _check_god_selected_event(self):
        # 命中天选且没有天选
        logger.debug("start _check_god_selected_event")
        if self.__is_god_selected() and not self.__has_god_selected_today():
            self.__roll = abs(self.__roll) * 3
            self.__set_god_selected()
            self.__message += "\n恭喜你触发了天选之人事件，点数转正并*3"

    def _check_double_roll_event(self):
        logger.debug("start _check_double_roll_event")
        if datetime.now().time().hour == self.DOUBLE_ROLL_TIME:
            self.__roll = self.__roll * 2
            self.__message += "\n触发了双倍时刻事件，点数*2"

    def _check_first_event(self):
        logger.debug("start _check_first_event")
        if not self.__has_first_man_today():
            self.__roll = abs(self.__roll) * 2
            self.__set_first_man_today()
            self.__message += "\n恭喜你触发了勤劳之人事件，点数转正并*2"

    def _handle_roll(self):
        self._check_manager_event()
        self._check_double_roll_event()
        self._check_god_selected_event()
        self._check_first_event()
        self.__handled = True
        self.__message += "\n最终点数为{}".format(self.__roll)

    def get_roll(self):
        if not self.__handled:
            self._handle_roll()
        return self.__roll

    def get_roll_message(self):
        return self.__message.format(self.__roll)
