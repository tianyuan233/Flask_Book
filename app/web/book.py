from flask import jsonify, request

from app.spider.exchange_book import ExangeBook
from app.libs.helper import is_isbn_or_key
from app.view_modules.book import BookViewModel
from . import web
from app.forms.book import SearchForm

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
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == 'isbn':
            result = ExangeBook.search_by_isbn(q)
            result = BookViewModel.package_single(result,q)
        else:
            result = ExangeBook.search_by_keyword(q,page)
            result = BookViewModel.package_collections(result,q)
        return jsonify(result)
    else:
        return jsonify(form.errors)
