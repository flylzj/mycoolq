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


class PythonLangRef(Base):
    __tablename__ = 'python_lang_ref'

    id =Column(Integer, primary_key=True, autoincrement=True)
    title1 = Column(String(64), nullable=False)
    title2 = Column(String(64), nullable=False)
    url = Column(String(256), nullable=False)


def find_lib(lib_name):
    session = SESSION()
    try:
        return session.query(PythonLibs).filter_by(name=lib_name).first()
    except Exception as e:
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
        pass
    finally:
        session.close()


def find_lang_ref(many=False, **kwargs):
    session = SESSION()
    try:
        res = session.query(PythonLangRef).filter_by(**kwargs)
        if not many:
            return res.first()
        else:
            return res.all()
    except Exception as e:
        return None
    finally:
        session.close()


def insert_lang_ref(**kwargs):
    session = SESSION()
    try:
        lang = session.query(PythonLangRef).filter_by(title1=kwargs.get('title1'), title2=kwargs.get('title2')).first()
        if lang:
            lang.update(**kwargs)
        else:
            lang = PythonLangRef(**kwargs)
            session.add(lang)
        session.commit()
    except Exception as e:
        pass
    finally:
        session.close()

