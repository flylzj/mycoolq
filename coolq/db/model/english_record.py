#coding: utf-8
from sqlalchemy import Column, String, Integer
from config import SESSION
from . import Base
import time
from datetime import datetime


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

