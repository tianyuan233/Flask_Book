from flask import Flask
from helper import is_isbn_or_key
app = Flask(__name__)
app.config.from_object('config')


@app.route('/book/search/<q>/<page>/')
def search(q, page):
    """

    :param q: 关键字或者 isbn
    :param page:
    :return:
    """
    isbn_or_key = is_isbn_or_key(q)



if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'],
            host='0.0.0.0',
            port='81')
