from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import login_manager
from app.libs.helper import is_isbn_or_key
from app.models.base import Base
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.exchange_book import ExBook


class User(UserMixin, Base):
    __tablename__ = 'user'
    # __bind_key__ = 'fisher'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    _password = Column('password', String(128), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)

    # 数据预处理 password
    # 属性读取
    @property
    def password(self):
        return self._password

    # 属性写入
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        exbook = ExBook()
        exbook.search_by_isbn(isbn)
        if not exbook.first:
            return False

        gifting = Gift.query.filter_by(uid=self.id,isbn=isbn,
                                       launched=False).first()

        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self,expiration=600):
        #序列化器
        s = Serializer(current_app.config['SECRET_KEY'],
                       expiration)

        pass





@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
