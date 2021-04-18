# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

ENGINE = create_engine('sqlite:///./data/data.db', echo=True)
SESSION = sessionmaker(bind=ENGINE)
Base = declarative_base()


