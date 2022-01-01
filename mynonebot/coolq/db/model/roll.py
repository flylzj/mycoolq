# coding: utf-8
from sqlalchemy import Column, Integer, func, desc, Text
from mynonebot.config import SESSION
from . import Base
import time
from datetime import datetime


class RollHistory(Base):

    __tablename__ = 'roll_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    point = Column(Integer, nullable=False)
    roll_time = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)


def count_toady_roll(**kwargs):
    session = SESSION()
    try:
        today_start = time.mktime(datetime.today().date().timetuple())
        today_end = today_start + 86400
        res = session.query(RollHistory).filter_by(**kwargs).filter(
            today_start < RollHistory.roll_time,
            today_end > RollHistory.roll_time
        )
        return res.count()
    except Exception as e:
        return 0
    finally:
        session.close()


def count_roll(group_id):
    most_point_user, most_point = count_most_point(group_id)
    most_times_user, most_times = count_most_times(group_id)
    return most_point_user, most_point, most_times_user, most_times


def count_my_roll(group_id, user_id):
    session = SESSION()
    try:
        res = session.query(func.sum(RollHistory.point).label('s')).filter_by(group_id=group_id, user_id=user_id).first()
        if res:
            return res[0]
        return 0
    except Exception as e:
        return 0
    finally:
        session.close()


# 最多点数
def count_most_point(group_id):
    session = SESSION()
    try:
        res = session.query(RollHistory.user_id, func.sum(RollHistory.point).label('s')).filter_by(group_id=group_id).group_by(RollHistory.user_id).order_by(desc('s')).first()
        if res:
            return res
        return 0, 0
    except Exception as e:
        return 0, 0
    finally:
        session.close()


# 最多次数
def count_most_times(group_id):
    session = SESSION()
    try:
        res = session.query(RollHistory.user_id, func.count(RollHistory.user_id).label('t')).filter_by(group_id=group_id).group_by(RollHistory.user_id).order_by(desc('t')).first()
        if res:
            return res
        return 0, 0
    except Exception as e:
        return 0, 0
    finally:
        session.close()


def insert_point(**kwargs):
    session = SESSION()
    try:
        roll = RollHistory(**kwargs)
        session.add(roll)
        session.commit()
    except Exception as e:
        return e
    finally:
        session.close()

