from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_modules.wish import MyWishes
from . import web

__author__ = '七月'


@web.route('/my/wish')
def my_wish():
    uid = current_user.id
    # 我添加到gift中的数据
    wishes_of_mine = Wish.get_my_wish(uid)
    # 我添加到gift中的书籍的isbn 返回一个列表
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    print(isbn_list)
    gift_count_list = Gift.get_gift_counts(isbn_list)
    print(gift_count_list)
    view_model = MyWishes(wishes_of_mine, gift_count_list)

    return render_template('my_wish.html', wishes=view_model.wishes)

    pass


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        # 事务 回滚
        # try:
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash('这本书已添加至你的礼物清单或已经存在与你的心愿清单')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
