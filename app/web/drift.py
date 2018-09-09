from flask import flash, url_for, redirect, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from app.forms.book import DriftForm
from app.libs.email import send_email
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_modules.book import BookViewModel
from . import web

__author__ = '七月'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的，不能跟自己索要哦~')
        return redirect(url_for('web.detail', isbn=current_gift.isbn))
    can = current_user.can_send_gift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_a_drift(form, current_gift)
        send_email(current_gift.user.email, '有人想要一本书', 'email/get_gift.html',
                   wisher=current_user,
                   gift=current_gift)
    gifter = current_gift.user.summary

    return render_template('drift.html',
                           gifter=gifter,
                           user_beans=current_user.beans,
                           form=form
                           )


@web.route('/pending')
def pending():
    # 查询条件的或关系
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id,
            Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    pass


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    pass


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    pass


def save_a_drift(drift_form, current_gift):
    with db.auto_commit():
        book = BookViewModel(current_gift.book)

        drift = Drift()
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn
        # 当请求生成时，不需要让这个礼物处于锁定状态
        # 这样赠送者是可以收到多个索取请求的，由赠送者选择送给谁
        # current_gift.launched = True
        # 请求者鱼豆-1
        current_user.beans -= 1
        # 但是赠送者鱼豆不会立刻+1
        # current_gift.user.beans += 1
        db.session.add(drift)
