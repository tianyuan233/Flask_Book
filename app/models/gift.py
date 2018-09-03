from flask import current_app
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.exchange_book import ExBook


class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_gift_counts(cls, isbn_list):
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.status == 1,
            Gift.isbn.in_(isbn_list)
        ).group_by(
            Gift.isbn
        ).all()
        count_list = [{'count': res[0], 'isbn': res[1]} for res in count_list]
        return count_list

    @classmethod
    def get_my_gift(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)
        ).all()
        return gifts

    @property
    def book(self):
        ex_book = ExBook()
        ex_book.search_by_isbn(self.isbn)
        return ex_book.first

    @classmethod
    def recent(cls):
        gift_list = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_PER_PAGE']).distinct().all()
        return gift_list
