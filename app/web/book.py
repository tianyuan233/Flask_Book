from flask import jsonify, request

from exchange_book import ExangeBook
from helper import is_isbn_or_key
from . import web


@web.route('/book/search')
def search():
    """

    :param q: 关键字或者 isbn
    :param page:
    :return:
    ?q=参数
    """
    q = request.args['q']
    isbn_or_key = is_isbn_or_key(q)
    if isbn_or_key == 'isbn':
        result = ExangeBook.search_by_isbn(q)
    else:
        result = ExangeBook.search_by_keyword(q)
    return jsonify(result)
