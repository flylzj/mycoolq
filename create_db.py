#coding: utf-8
from config import ENGINE
# 显式导入table才能create
from coolq.db.model.new_member_captcha import NewMemberCaptcha
from coolq.db.model.python_lib_helper import PythonLibs
from coolq.db.model import Base

def init_db(new=False):
    if new:
        Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)

if __name__ == '__main__':
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)