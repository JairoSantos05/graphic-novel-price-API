from fastapi import FastAPI

app = FastAPI()

products = [
    {
        "isbn": "9781779516992",
        "title": "Batman Vol. 1",
        "lowest_price": 14.99
    },
    {
        "isbn": "9781779521149",
        "title": "Nightwing Vol. 1",
        "lowest_price": 12.99
    }
]

@app.get("/")
def root():
    return {"message": "Graphic Novel Price Tracker API"}

@app.get("/products")
def get_products():
    return products

@app.get("/products/{isbn}")
def get_product(isbn: str):
    for product in products:
        if product["isbn"] == isbn:
            return product

    return {"error": "Product not found"}