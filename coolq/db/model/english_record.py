#coding: utf-8
from sqlalchemy import Column, String, Integer
from config import SESSION
from . import Base
import time
from datetime import datetime
import calendar


class EnglishRecord(Base):

    __tablename__ = 'english_record'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(11), nullable=False)
    record_datetime = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    days = Column(Integer, nullable=False)
    url = Column(String(256), nullable=False, index=True)

    def get_date(self):
        t = time.gmtime(self.record_datetime + 8 * 3600)  # UTC+8
        return t

def search_history(url):
    try:
        session = SESSION()
        res = session.query(EnglishRecord).filter_by(url=url).first()
        return res
    except Exception as e:
        pass

def get_recorded_today():
    # 今天打卡了的
    try:
        session = SESSION()
        d = datetime.today().date().timetuple()
        res = session.query(EnglishRecord).filter(
            time.mktime(d) < EnglishRecord.record_datetime,
            time.mktime(d) + 86399 > EnglishRecord.record_datetime # 当天时间
        ).all()
        return res
    except Exception as e:
        pass

def count_recorded(user_id):
    try:
        session = SESSION()
        d = datetime.today().today()
        month_start_d = datetime(year=d.year, month=d.month, day=1).timetuple()
        month_end_d = datetime(year=d.year, month=d.month, day=calendar.monthrange(year=d.year, month=d.month)[-1]).timetuple()
        res = session.query(EnglishRecord).filter(
            time.mktime(month_start_d) < EnglishRecord.record_datetime,
            time.mktime(month_end_d) + 86399 > EnglishRecord.record_datetime,  # 当天时间,
            EnglishRecord.user_id == user_id
        ).all()
        word_count = sum([record.word_count for record in res])
        days_this_month = len(res)
        days_total = res[-1].days
        return word_count, days_this_month, days_total
    except Exception as e:
        pass

