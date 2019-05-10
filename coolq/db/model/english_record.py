#coding: utf-8
from sqlalchemy import Column, String, Integer
from config import SESSION
from . import Base
import time
from datetime import datetime
import datetime as dt


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
            time.mktime(d) + 86399 > EnglishRecord.record_datetime  # 当天时间
        ).all()
        return res
    except Exception as e:
        pass


def get_statistics_data(month=True):
    # 要统计的数据有
    # 打卡天数，总单词数量，平均单词数量
    try:
        session = SESSION()
        if month:
            today = datetime.today()
            this_month = datetime(today.year, today.month, 1)
            if this_month.month < 12:
                next_month = datetime(today.year, today.month + 1, 1)
            else:
                next_month = datetime(today.year + 1, 1, 1)
            res = session.query(EnglishRecord).filter(
                time.mktime(this_month.timetuple()) <= EnglishRecord.record_datetime,
                time.mktime(next_month.timetuple()) > EnglishRecord.record_datetime
            ).all()
        else:
            res = session.query(EnglishRecord).all()
        data = dict()
        for record in res:
            if not data.get(record.user_id):
                data[record.user_id] = dict()
                data[record.user_id]["days"] = 1
                data[record.user_id]["word_count"] = record.word_count
            else:
                data[record.user_id]["days"] += 1
                data[record.user_id]["word_count"] += record.word_count
            data[record.user_id]["avg_word_count "] = \
                data.get(record.user_id).get("days") / data.get(record.user_id).get("word_count")
        return data
    except Exception as e:
        pass
