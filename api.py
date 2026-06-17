from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from dbqueries import (get_prices_for_book, best_deals, price_history)
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/book/{isbn}/prices")
def book_prices(isbn: int):
    """Get cheapest price for a book given isbn."""
    return get_prices_for_book(isbn)

@app.get("/deals", response_model=List[Deal])
def get_deals(limit: int = 10):
    """Get the absolute cheapest book prices tracked across the entire system."""
    raw_deals = best_deals(limit)
    
    formatted_deals = [
        Deal(isbn=row[0], retailer=row[1], price=row[2]) 
        for row in raw_deals
    ]
    return formatted_deals

@app.get("/book/{isbn}/history", response_model=BookHistoryResponse)
def book_price_history(isbn: int):
    """Returns every recorded price change over time for a graphic novel."""
    raw_history = price_history(isbn)
    
    formatted_history = []
    for row in raw_history:
        if row[2] is not None:
            formatted_history.append(
                PriceHistoryPoint(
                    date=str(row[0]), 
                    retailer=row[1],
                    price=row[2]
                )
            )
            
    return BookHistoryResponse(isbn=isbn, history=formatted_history)