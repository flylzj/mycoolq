# coding: utf-8
from sqlalchemy import Column, Integer
from mynonebot.config import SESSION
from . import Base
from datetime import datetime


class SignHistory(Base):

    __tablename__ = "sign_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    sign_time = Column(Integer, nullable=False)


def sign(user_id):
    session = SESSION()
    try:
        now = int(datetime.now().timestamp())
        history = SignHistory(
            user_id=user_id,
            sign_time=now
        )
        session.add(history)
        session.commit()
        return True
    except Exception as e:
        return False
    finally:
        session.close()


def has_signed_today(user_id):
    session = SESSION()
    try:
        today_begin = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        d = session.query(SignHistory).filter_by(user_id=user_id).filter(
            SignHistory.sign_time > today_begin
        ).first()
        if d:
            return True
        else:
            return False
    except Exception as e:
        return False
    finally:
        session.close()


