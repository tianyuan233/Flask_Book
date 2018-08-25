import json

from flask import request, render_template, flash

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.spider.exchange_book import ExBook
from app.view_modules.book import BookCollection, BookViewModel
from . import web


@web.route('/book/search')
def search():
    """

    :param q: 关键字或者 isbn
    :param page:
    :return:
    ?q=参数
    """
    # q = request.args['q']
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

        # return json.dumps(books, default=lambda o:o.__dict__)
    else:
        flash('搜索的关键字未找到，请重新搜索')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    """
    :param isbn: isbn为参数
    :return:
    """
    ex_book = ExBook()
    ex_book.search_by_isbn(isbn)
    book = BookViewModel(ex_book.first)
    return render_template('book_detail.html', book=book, wishes=[],gifts=[])

