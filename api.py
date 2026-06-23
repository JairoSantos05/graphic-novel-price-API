from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from dbqueries import (get_prices_for_book, best_deals, price_history)
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

#Model for the json structure expected from the frontend or structure returned by api
class Price(BaseModel):
    retailer: str
    price: float

class Product(BaseModel):
    isbn: int
    title: str
    prices: List[Price]
    lowest_price: float

class Deal(BaseModel):
    isbn: int
    retailer: str
    price: float

class PriceRange(BaseModel):
    lowest_price: float | None
    highest_price: float | None

class PriceHistoryPoint(BaseModel):
    date: str
    retailer: str
    price: float | None

class BookHistoryResponse(BaseModel):
    isbn: int
    history: List[PriceHistoryPoint]

app = FastAPI()

#Cross origin resource sharing (CORS) allows for frontend (Vercel) to send HTTP request to API (Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Route to search for specific books using a string text or exact ISBN number
@app.get("/book/{search_term}/prices")
def read_prices(search_term: str):
    return get_prices_for_book(search_term)

# Route to fetch today's top discounted book records for the homepage grid
@app.get("/deals")
def read_deals(limit: int = 150):
    return best_deals(limit)

#Route to gather history tracking log data for history timeline
@app.get("/book/{isbn}/history")
#Enforces int to protect against invalid inputs
def read_history(isbn: int):
    return price_history(isbn)