#coding: utf-8
# 显式导入table才能create
from coolq_nonebot2.db.models import Days, RollEvent, RollHistory
from coolq_nonebot2.db import Base, ENGINE


def init_db(new=False):
    if new:
        Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)


if __name__ == '__main__':
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)