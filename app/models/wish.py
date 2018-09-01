from sqlalchemy import Column, Boolean, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db


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
