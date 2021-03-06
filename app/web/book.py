from flask import request, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.exchange_book import ExBook
from app.view_modules.book import BookCollection, BookViewModel
from app.view_modules.trade import TradeInfo
from . import web


@web.route('/book/search')
def search():
    """
    :param q: 关键字或者 isbn
    :param page:
    :return:
    ?q=参数
    """
    form = SearchForm(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        ex_book = ExBook()
        if isbn_or_key == 'isbn':
            ex_book.search_by_isbn(q)
        else:
            ex_book.search_by_keyword(q, page)
        books.fill(ex_book, q)
    else:
        flash('搜索的关键字未找到，请重新搜索')
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    """
    :param isbn: isbn为参数
    :return:
    """
    has_in_gifts = False
    has_in_wishes = False

    if current_user.is_authenticated:
        # 如果未登录，current_user将是一个匿名用户对象
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()

    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)

    ex_book = ExBook()
    ex_book.search_by_isbn(isbn)
    book = BookViewModel(ex_book.first)
    return render_template('book_detail.html', book=book,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes)
