# coding: utf-8
from sqlalchemy import Column, Integer, func, desc
from config import SESSION
from . import Base
import time
from datetime import datetime
from coolq.util.coolq import at_someone


class RollHistory(Base):

    __tablename__ = 'roll_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    point = Column(Integer, nullable=False)
    roll_time = Column(Integer, nullable=False)


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
    message = ""
    if not most_point_user:
        message += "本群暂无点数之王\n"
    else:
        message += f"本群点数之王:{at_someone(most_point_user)}\n已掷骰子点数总和:{most_point}"
    if not most_times_user:
        message += "本群暂无次数之王\n"
    else:
        message += f"本群次数之王:{at_someone(most_times_user)}\n已掷骰子次数:{most_times}"
    return message

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

