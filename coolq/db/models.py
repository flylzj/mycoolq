# coding: utf-8
from sqlalchemy import Column, Integer, func, desc, Text, String
from sqlalchemy import update, select
from . import Base, SESSION
from coolq.util.lib import get_today_start_end
from nonebot.log import logger
import enum


class Days(Base):
    __tablename__ = 'days'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    comment = Column(String(255))
    days = Column(Integer, nullable=False, default=0)

    @staticmethod
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

    @staticmethod
    def increase_one(user_id):
        session = SESSION()
        try:
            d = session.query(Days).filter_by(user_id=user_id).first()
            if not d:
                return
            d.days += 1
            session.commit()
        except Exception as e:
            session.rollback()
        finally:
            session.close()

    @staticmethod
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


class RollEventEnum(enum.IntEnum):
    god_select_event = 0
    double_event = 1
    first_man_event = 2
    manager_event = 3

    @property
    def int_value(self):
        return self.value


class RollHistory(Base):

    __tablename__ = 'roll_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, nullable=False)
    user_id = Column(String(64), nullable=False)
    point = Column(Integer, nullable=False)
    roll_time = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)

    @staticmethod
    def count_toady_roll(**kwargs):
        session = SESSION()
        try:
            today_start, today_end = get_today_start_end()
            res = session.query(RollHistory).filter_by(**kwargs).filter(
                today_start < RollHistory.roll_time,
                today_end > RollHistory.roll_time
            )
            return res.count()
        except Exception as e:
            return 0
        finally:
            session.close()

    @staticmethod
    def count_roll(group_id):
        most_point_user, most_point = RollHistory.count_most_point(group_id)
        most_times_user, most_times = RollHistory.count_most_times(group_id)
        return most_point_user, most_point, most_times_user, most_times

    @staticmethod
    def count_my_roll(group_id, user_id):
        session = SESSION()
        try:
            res = session.query(RollHistory, func.sum(RollHistory.point)).filter_by(
                group_id=group_id,
                user_id=user_id
            ).first()
            if res:
                return res[1]
            return 0
        except Exception as e:
            logger.error("count_my_roll err {}".format(str(e)), exc_info=True)
            return 0
        finally:
            session.close()

    # 最多点数
    @staticmethod
    def count_most_point(group_id):
        session = SESSION()
        try:
            statement = select(RollHistory.user_id, func.sum(RollHistory.point)).filter_by(
                group_id=group_id
            ).group_by(
                RollHistory.user_id
            ).order_by(desc(func.sum(RollHistory.point)))
            res = session.execute(statement).first()
            print(res)
            if res:
                return res
            return 0, 0
        except Exception as e:
            logger.error("count_most_point err {}".format(str(e)))
            return 0, 0
        finally:
            session.close()

    # 最多次数
    @staticmethod
    def count_most_times(group_id):
        session = SESSION()
        try:
            statement = select(RollHistory.user_id, func.count(RollHistory.user_id)).filter_by(
                group_id=group_id
            ).group_by(
                RollHistory.user_id
            ).order_by(desc(func.count(RollHistory.user_id)))
            res = session.execute(statement).first()
            if res:
                return res
            return 0, 0
        except Exception as e:
            logger.error("count_most_times err {}".format(str(e)), exc_info=True)
            return 0, 0
        finally:
            session.close()

    @staticmethod
    def insert_point(**kwargs):
        session = SESSION()
        try:
            roll = RollHistory(**kwargs)
            session.add(roll)
            session.commit()
            session.refresh(roll)
            return roll.id
        except Exception as e:
            logger.error("insert_point err {}".format(str(e)), exc_info=True)
            return 0
        finally:
            session.close()

    @staticmethod
    def update_roll(roll_id, roll, message):
        session = SESSION()
        try:
            logger.debug("update_roll for roll_id {} roll {} message {}".format(roll_id, roll, message))
            stmt = update(RollHistory).where(RollHistory.id == roll_id).values(
                point=roll,
                message=message
            ).execution_options(synchronize_session="fetch")
            _ = session.execute(stmt)
            session.commit()
        except Exception as e:
            logger.error("update_roll err {}".format(str(e)))
        finally:
            session.close()


class RollEvent(Base):
    __tablename__ = "roll_event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    roll_id = Column(Integer, nullable=False)
    group_id = Column(Integer, nullable=False)
    user_id = Column(String(64), nullable=False)
    event_type = Column(Integer, nullable=False)
    event_time = Column(Integer, nullable=False)

    @staticmethod
    def has_god_select_man_today(group_id):
        start, end = get_today_start_end()
        return RollEvent.has_event(group_id=group_id, event_type=RollEventEnum.god_select_event.int_value, start=start, end=end)

    @staticmethod
    def has_first_man_today(group_id):
        start, end = get_today_start_end()
        return RollEvent.has_event(group_id=group_id, event_type=RollEventEnum.first_man_event.int_value, start=start, end=end)

    @staticmethod
    def has_event(group_id, event_type, start=0, end=0):
        session = SESSION()
        try:
            res = session.query(RollEvent).filter_by(
                event_type=event_type,
                group_id=group_id,
            )
            if start != 0 and end != 0:
                res = res.filter(
                    start < RollEvent.event_time,
                    end > RollEvent.event_time
                )
            if res.first():
                return True
            else:
                return False
        except Exception as e:
            logger.error("has_event err" + str(e), exc_info=True)
            return False
        finally:
            session.close()

    @staticmethod
    def insert_event(**kwargs):
        logger.info("event {}".format(kwargs))
        session = SESSION()
        try:
            event = RollEvent(**kwargs)
            session.add(event)
            session.commit()
            session.refresh(event)
            return event.id
        except Exception as e:
            logger.error("insert_event err" + str(e), exc_info=True)
            return 0
        finally:
            session.close()


class SignInAccountEnum(enum.IntEnum):
    t00ls_account = 0

    @property
    def int_value(self):
        return self.value


class SignInAccount(Base):
    __tablename__ = "sign_in_account"

    id = Column(Integer, autoincrement=True, primary_key=True)
    account_type = Column(Integer, nullable=False)
    user_id = Column(String(64), nullable=False)
    account_info = Column(String(255), nullable=False, default="{}")  # 默认空json

    @staticmethod
    def insert_account(**kwargs):
        session = SESSION()
        try:
            account = SignInAccount(**kwargs)
            session.add(account)
            session.commit()
            session.flush(account)
            return account.id
        except Exception as e:
            logger.error(f"insert_account err {str(e)}")
            return

    @staticmethod
    def get_accounts(account_type, user_id=""):
        session = SESSION()
        try:
            statement = select(SignInAccount).filter_by(
                account_type=account_type
            )
            if user_id:
                statement = statement.filter_by(
                    user_id=user_id,
                )
            res = session.execute(statement).scalars().all()
            for r in res:
                yield r
        except Exception as e:
            logger.error(f"get_accounts err {str(e)}")

    @staticmethod
    def update_account(user_id, account_id, **data):
        session = SESSION()
        try:
            update_statement = update(SignInAccount).where(id=account_id, user_id=user_id).update(**data)
            res = session.execute(update_statement)
            return res
        except Exception as e:
            logger.error(f"modify_account err {str(e)}")