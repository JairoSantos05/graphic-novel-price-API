def get_all_products():
    return [
        {
            "isbn": "9781779516992",
            "title": "Batman Vol. 1",
            "lowest_price": 12.99
        },
        {
            "isbn": "9781779521149",
            "title": "Nightwing Vol. 1",
            "lowest_price": 15.99
        }
    ]

def get_product(isbn: str):
    products = get_all_products()

    for product in products:
        if product["isbn"] == isbn:
            return product

    return None