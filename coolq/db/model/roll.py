# coding: utf-8
from sqlalchemy import Column, Integer, String
from config import SESSION
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

