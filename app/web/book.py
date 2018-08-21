import json

from flask import jsonify, request, render_template

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.spider.exchange_book import ExBook
from app.view_modules.book import BookCollection
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
        return json.dumps(books, default=lambda o:o.__dict__)
    else:
        return jsonify(form.errors)

@web.route('/test/')
def test():
    r = {
        'name':'zty',
        'age':'18'
    }

    return render_template('test.html',data=r)