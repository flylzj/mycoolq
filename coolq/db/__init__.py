# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

ENGINE = create_engine('sqlite:///./data/data.db')
SESSION = sessionmaker(bind=ENGINE)
Base = declarative_base()


def init_db(new=False):
    if new:
        Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)


