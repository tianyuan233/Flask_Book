from flask import current_app
from sqlalchemy import Column, Boolean, String, Integer, ForeignKey, func, desc
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.exchange_book import ExBook


class Wish(Base):
    __tablename__ = 'wish'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_wish_counts(cls, isbn_list):
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.status == 1,
            Wish.isbn.in_(isbn_list)
        ).group_by(
            Wish.isbn
        ).all()
        count_list = [{'count': res[0], 'isbn': res[1]} for res in count_list]
        return count_list
    #######
    @classmethod
    def get_my_wish(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)
        ).all()
        return wishes

    @property
    def book(self):
        ex_book = ExBook()
        ex_book.search_by_isbn(self.isbn)
        return ex_book.first

    @classmethod
    def recent(cls):
        wish_list = Wish.query.filter_by(
            launched=False).group_by(
            Wish.isbn).order_by(
            desc(Wish.create_time)).limit(
            current_app.config['RECENT_BOOK_PER_PAGE']).distinct().all()
        # view_model = GiftsViewModel.recent(gift_list)
        return wish_list