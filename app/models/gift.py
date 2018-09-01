from flask import current_app
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, desc
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.spider.exchange_book import ExBook


class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

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
        # view_model = GiftsViewModel.recent(gift_list)
        return gift_list
