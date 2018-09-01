from flask import current_app, flash, redirect, url_for
from flask_login import login_required, current_user

from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from . import web


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    #我添加到gift中的数据
    gifts_of_mine = Gift.get_my_gift(uid)

    isbn_list = [gift.isbn for gift in gifts_of_mine]
    print(isbn_list)
    wish_count_list = Wish.get_wish_counts(isbn_list)
    print(wish_count_list)
    return 'test'


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # 事务 回滚
        # try:
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_BOOK']
            db.session.add(gift)
    else:
        flash('这本书已添加至你的礼物清单或已经存在与你的心愿清单')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
