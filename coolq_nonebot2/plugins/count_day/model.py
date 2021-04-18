# coding: utf-8
from sqlalchemy import Column, Integer, String
from coolq_nonebot2.db import Base


class Days(Base):

    __tablename__ = 'days'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    comment = Column(String(255))
    days = Column(Integer, nullable=False, default=0)
