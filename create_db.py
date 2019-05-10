#coding: utf-8
from config import ENGINE
# 显式导入table才能create
from coolq.db.model.english_record import EnglishUser, EnglishRecord
from coolq.db.model import Base

if __name__ == '__main__':
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)
