# coding: utf-8
from sqlalchemy import Column, Integer, String
from config import SESSION
from . import Base
from random import randint
import time


class NewMemberCaptcha(Base):
    __tablename__ = 'new_member_captcha'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # group id which he was new
    group_id = Column(Integer, nullable=False)
    # user id（qq）
    user_id = Column(Integer, nullable=False)
    # code
    verify_code = Column(Integer, nullable=False)
    # insert time
    insert_time = Column(Integer, nullable=False)
    # is verify（0 is not verify, 1 is verified）
    is_verify = Column(Integer, nullable=False, default=0)


class Flag(Base):
    __tablename__ = 'flag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    flag = Column(String(256))


def gen_code():
    return randint(100000, 999999)


def insert_new_captcha(**kwargs):
    '''

    :param kwargs: group_id, user_id, verify_code
    :return:
    '''
    nmc = NewMemberCaptcha(**kwargs)
    session = SESSION()
    try:
        session.add(nmc)
        session.commit()
    except Exception as e:
        pass
    finally:
        session.close()


def search_captcha(**kwargs):
    session = SESSION()
    try:
        return session.query(NewMemberCaptcha).filter_by(**kwargs).first()
    except Exception as e:
        return None
    finally:
        session.close()


def verify(group_id, user_id, code):
    session = SESSION()
    try:
        nmc = session.query(NewMemberCaptcha).filter_by(group_id=group_id, user_id=user_id, is_verify=0).first()
        if not nmc:
            # sql = '''
            # SELECT id FROM new_member_captcha WHERE verify_code={}
            # '''.format(code)
            # res = session.execute(sql)
            # message = ""
            # for r in res:
            #     message += str(r)
            return "没有你的验证码"
        if code != str(nmc.verify_code):
            return "验证码错误"
        nmc.is_verify = 1
        session.commit()
        return "验证成功, 环境问题参考群文件“从零开始的Python环境配置.rar”。Python安装包、VSCode安装包、Pycharm安装包都可以在群文件找到，按需自取。试着对我说:help"
    except Exception as e:
        return str(e)
    finally:
        session.close()


def find_out_date():
    session = SESSION()
    try:
        return session, session.query(NewMemberCaptcha).filter(
            time.time() - NewMemberCaptcha.insert_time > 300,
            NewMemberCaptcha.is_verify == 0
        ).all()
    except Exception as e:
        return session, []

def is_verifying(group_id, user_id):
    return search_captcha(group_id=group_id, user_id=user_id, is_verify=0)



