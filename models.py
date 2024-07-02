from database import Base
from sqlalchemy import Column, String, Integer


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    hashed_password = Column(String)
    email = Column(String, unique=True)


class Texts(Base):
    __tablename__ = 'texts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
