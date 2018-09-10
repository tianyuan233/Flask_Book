from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_modules.gift import MyGifts
from . import web


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    # 我添加到gift中的数据
    gifts_of_mine = Gift.get_my_gift(uid)
    # 我添加到gift中的书籍的isbn 返回一个列表
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    print(isbn_list)
    wish_count_list = Wish.get_wish_counts(isbn_list)
    print(wish_count_list)
    view_model = MyGifts(gifts_of_mine, wish_count_list)

    return render_template('my_gifts.html',gifts=view_model.gifts)

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
    gift = Gift.query.filter_by(id=gid, launched=False).first()
    if not gift:
        flash('该书籍不存在，或已经交易，删除失败')
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处于交易状态，请先前往鱼漂完成该交易')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))
