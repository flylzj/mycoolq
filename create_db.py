#coding: utf-8
# 显式导入table才能create
from coolq.db.models import Days, RollEvent, RollHistory
from coolq.db import Base, ENGINE


def init_db(new=False):
    if new:
        Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)


if __name__ == '__main__':
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)