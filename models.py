from database import Base
from sqlalchemy import Column, String, Integer


class Texts(Base):
    __tablename__ = 'texts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
