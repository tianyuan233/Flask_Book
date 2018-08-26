from sqlalchemy import Column, Integer, String

from app.models.base import db


class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(20))  # 装订版本
    publish = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)  # 页数
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))
