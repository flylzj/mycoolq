# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot import driver
from sqlalchemy.ext.declarative import declarative_base

ENGINE = create_engine(driver.config.db_url, echo=True)
SESSION = sessionmaker(bind=ENGINE)

Base = declarative_base()
