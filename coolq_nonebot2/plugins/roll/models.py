# coding: utf-8
from sqlalchemy import Column, Integer, func, desc, Text
from coolq_nonebot2.db import Base, SESSION
from coolq_nonebot2.util.lib import get_today_start_end
from nonebot.log import logger
import enum


class RollEventEnum(enum.Enum):
    god_select_event = 0
    double_event = 1
    first_man_event = 2
    manager_event = 3


class RollHistory(Base):

    __tablename__ = 'roll_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    point = Column(Integer, nullable=False)
    roll_time = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)

    @staticmethod
    def count_toady_roll(**kwargs):
        session = SESSION()
        try:
            today_start, today_end = get_today_start_end()
            res = session.query(RollHistory).filter_by(**kwargs).filter(
                today_start < RollHistory.roll_time,
                today_end > RollHistory.roll_time
            )
            return res.count()
        except Exception as e:
            return 0
        finally:
            session.close()

    @staticmethod
    def count_roll(group_id):
        most_point_user, most_point = RollHistory.count_most_point(group_id)
        most_times_user, most_times = RollHistory.count_most_times(group_id)
        return most_point_user, most_point, most_times_user, most_times

    @staticmethod
    def count_my_roll(group_id, user_id):
        session = SESSION()
        try:
            res = session.query(func.sum(RollHistory.point).label('s')).filter_by(group_id=group_id,
                                                                                  user_id=user_id).first()
            if res:
                return res[0]
            return 0
        except Exception as e:
            return 0
        finally:
            session.close()

    # 最多点数
    @staticmethod
    def count_most_point(group_id):
        session = SESSION()
        try:
            res = session.query(RollHistory.user_id, func.sum(RollHistory.point).label('s')).filter_by(
                group_id=group_id).group_by(RollHistory.user_id).order_by(desc('s')).first()
            if res:
                return res
            return 0, 0
        except Exception as e:
            return 0, 0
        finally:
            session.close()

    # 最多次数
    @staticmethod
    def count_most_times(group_id):
        session = SESSION()
        try:
            res = session.query(RollHistory.user_id, func.count(RollHistory.user_id).label('t')).filter_by(
                group_id=group_id).group_by(RollHistory.user_id).order_by(desc('t')).first()
            if res:
                return res
            return 0, 0
        except Exception as e:
            return 0, 0
        finally:
            session.close()

    @staticmethod
    def insert_point(**kwargs):
        session = SESSION()
        try:
            roll = RollHistory(**kwargs)
            session.add(roll)
            session.commit()
            return roll.id
        except Exception as e:
            logger.error("insert_point err {}".format(str(e)), exc_info=True)
            return 0
        finally:
            session.close()


class RollEvent(Base):
    __tablename__ = "roll_event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    roll_id = Column(Integer, nullable=False)
    group_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    event_type = Column(Integer, nullable=False)
    event_time = Column(Integer, nullable=False)

    @staticmethod
    def has_god_select_man_today(group_id):
        start, end = get_today_start_end()
        return RollEvent.has_event(group_id=group_id, event_type=RollEventEnum.god_select_event, start=start, end=end)

    @staticmethod
    def has_first_man_today(group_id):
        start, end = get_today_start_end()
        return RollEvent.has_event(group_id=group_id, event_type=RollEventEnum.first_man_event, start=start, end=end)

    @staticmethod
    def has_event(group_id, event_type, start=0, end=0):
        session = SESSION()
        try:
            res = session.query(RollEvent).filter_by(
                event_type=event_type,
                group_id=group_id,
            )
            if start != 0 and end != 0:
                res = res.filter(
                    start < RollEvent.event_time,
                    end > RollEvent.event_time
                )
            if res.first():
                return True
            else:
                return False
        except Exception as e:
            logger.error("has_event err" + str(e), exc_info=True)
            return False
        finally:
            session.close()

    @staticmethod
    def insert_event(**kwargs):
        session = SESSION()
        try:
            roll = RollEvent(**kwargs)
            session.add(roll)
            session.commit()
        except Exception as e:
            logger.error("insert_event err" + str(e), exc_info=True)
        finally:
            session.close()



