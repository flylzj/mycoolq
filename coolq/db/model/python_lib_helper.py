# coding: utf-8
from sqlalchemy import Column, Integer, String
from config import SESSION
from . import Base


class PythonLibs(Base):
    __tablename__ = 'python_libs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64), nullable=False)
    name = Column(String(64), nullable=False, unique=True)
    comment = Column(String(128), nullable=False)
    url = Column(String(256), nullable=False)

    def update(self, **kwargs):
        self.title = kwargs.get('title')
        self.name = kwargs.get('name')
        self.comment = kwargs.get('comment')
        self.url = kwargs.get('url')


def find_lib(lib_name):
    session = SESSION()
    try:
        return session.query(PythonLibs).filter_by(name=lib_name).first()
    except Exception as e:
        print(e)
        return None
    finally:
        session.close()


def insert_lib(**kwargs):
    session = SESSION()
    try:
        lib = session.query(PythonLibs).filter_by(name=kwargs.get('lib_name')).first()
        if lib:
            lib.update(**kwargs)

        else:
            lib = PythonLibs(**kwargs)
            session.add(lib)
        session.commit()
    except Exception as e:
        print(e)
    finally:
        session.close()

