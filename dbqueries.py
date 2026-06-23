from db import connection

def get_prices_for_book(search_term: str):
    conn = connection()
    cursor = conn.cursor()

    #Joins price values to their text labels, filters out NULL or 0 values, 
    # and selects only the absolute latest scraper date entry for each retailer row.
    query = """
        SELECT p.retailer, p.price, p.url, g.title, p.isbn 
        FROM Prices p
        LEFT JOIN graphic_novels g ON p.isbn = g.isbn
        WHERE (p.isbn = ? OR g.title LIKE ?)
          AND p.price IS NOT NULL 
          AND p.price > 0
          AND p.date = (SELECT MAX(date) FROM Prices WHERE isbn = p.isbn AND retailer = p.retailer)
        ORDER BY p.price ASC
    """
    cursor.execute(query, (search_term, f"%{search_term}%"))
    rows = cursor.fetchall()
    conn.close()
    
    #Standardizes the raw SQL output table grid layout into JSON objects for React
    formatted_results = []
    for row in rows:
        formatted_results.append({
            "retailer": row[0],
            "price": row[1],
            "url": row[2],
            "title": row[3] if row[3] else f"Graphic Novel ({row[4]})",
            "isbn": row[4]
        })
    return formatted_results


def best_deals(limit: int):
    conn = connection()
    cursor = conn.cursor()
    query = """
        SELECT p.isbn, p.retailer, p.price, g.title, p.url
        FROM Prices p
        LEFT JOIN graphic_novels g ON p.isbn = g.isbn
        WHERE p.price IS NOT NULL 
          AND p.price > 0
          AND p.date = (SELECT MAX(date) FROM Prices WHERE isbn = p.isbn AND retailer = p.retailer)
        ORDER BY p.price ASC
        LIMIT ?
    """
    cursor.execute(query, (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    formatted_results = []
    for row in rows:
        formatted_results.append({
            "isbn": row[0],
            "retailer": row[1],
            "price": row[2],
            "title": row[3] if row[3] else f"Graphic Novel ({row[0]})",
            "url": row[4]
        })
    return formatted_results


def price_history(isbn):
    conn = connection()
    cursor = conn.cursor()
    
    # Gathers all points across all tracking dates from oldest to newest
    query = """
        SELECT p.date, p.retailer, p.price, g.title
        FROM Prices p
        LEFT JOIN graphic_novels g ON p.isbn = g.isbn
        WHERE (p.isbn = ? OR p.isbn = CAST(? AS TEXT))
          AND p.price IS NOT NULL 
          AND p.price > 0
        ORDER BY p.date ASC
    """
    
    cursor.execute(query, (isbn, str(isbn)))
    rows = cursor.fetchall()
    conn.close()
    
    history_list = []
    for row in rows:
        history_list.append({
            "date": row[0],
            "retailer": row[1],
            "price": row[2],
            "title": row[3] if row[3] else f"Graphic Novel ({isbn})"
        })
    return {"isbn": isbn, "history": history_list}