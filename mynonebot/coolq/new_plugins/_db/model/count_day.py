# coding: utf-8
from sqlalchemy import Column, Integer, String
from mynonebot.config import SESSION
from . import Base


class Days(Base):

    __tablename__ = 'days'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    comment = Column(String(255))
    days = Column(Integer, nullable=False, default=0)


def to_zero(user_id):
    session = SESSION()
    try:
        d = session.query(Days).filter_by(user_id=user_id).first()
        if not d:
            d = Days(
                user_id=user_id,
                days=0
            )
            session.add(d)
            session.commit()
            return
        d.days = 0
        session.commit()
        return True
    except Exception as e:
        session.rollback()
    finally:
        session.close()


def increase_one(user_id):
    session = SESSION()
    try:
        d = session.query(Days).filter_by(user_id=user_id).first()
        if not d:
            return
        d.days += 1
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()


def get_need_increase():
    session = SESSION()
    try:
        days = session.query(Days).all()
        for d in days:
            yield d
    except Exception as e:
        pass
    finally:
        session.close()