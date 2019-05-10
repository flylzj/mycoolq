#coding: utf-8
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config import SESSION
from . import Base
import time
from datetime import datetime
import calendar


class EnglishUser(Base):

    __tablename__ = 'english_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(11), nullable=False)
    nickname = Column(String(64))


class EnglishRecord(Base):

    __tablename__ = 'english_record'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(11), ForeignKey(EnglishUser.user_id), nullable=False)
    record_datetime = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    days = Column(Integer, nullable=False)
    url = Column(String(256), nullable=False, index=True)

    user = relationship('EnglishUser', backref='records')

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
        start_date = time.strftime("%Y-%m-%d", time.localtime())
        end_date = ""
        for record in res:
            user_info = (record.user_id, record.user.nickname)
            if not data.get(user_info):
                data[user_info] = {}
            d = time.strftime("%Y-%m-%d", time.localtime(record.record_datetime))
            data[user_info][d] = record.word_count
            if d < start_date:
                start_date = d
            if d > end_date:
                end_date = d
        end_date_second = time.mktime(time.strptime(end_date, '%Y-%m-%d'))
        start_date_second = time.mktime(time.strptime(start_date, '%Y-%m-%d'))
        seconds = end_date_second - start_date_second
        days_count = int(seconds / (3600 * 24))
        days = []
        for i in range(days_count + 1):
            days.append(time.strftime("%Y-%m-%d", time.localtime(start_date_second + i * (3600 * 24))))
        for day in days:
            for user in data:
                if not data.get(user).get(day):
                    data[user][day] = 0
        return data
    except Exception as e:
        pass

