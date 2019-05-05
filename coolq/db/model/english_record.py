#coding: utf-8
from sqlalchemy import Column, String, Integer, DateTime
from . import Base
import time


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