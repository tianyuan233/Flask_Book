class BookViewModel:
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword

        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__book_cut_data(data)]

        return returned

    @classmethod
    def package_collections(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword

        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__book_cut_data(book) for book in data['books']]

        return returned

    @classmethod
    def __book_cut_data(cls, data):
        book = {
            'title':data['title'],
            'publisher':data['publisher'],
            'pages':data['pages'] or '',
            'author':','.join(data['author']),
            'price':data['price'],
            'summary':data['summary'] or '',
            'image':data['image']
        }
        return book
