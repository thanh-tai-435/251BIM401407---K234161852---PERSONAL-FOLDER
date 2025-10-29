import os
os.makedirs("output", exist_ok=True)
# query_customer.py
from connector.connector import Connector

def customers_by_film(conn):
    sql = """
    SELECT 
        f.title AS film_title,
        GROUP_CONCAT(DISTINCT CONCAT(c.first_name, ' ', c.last_name) SEPARATOR ', ') AS customers
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    JOIN customer c ON r.customer_id = c.customer_id
    GROUP BY f.title
    ORDER BY f.title;
    """
    df = conn.queryDataset(sql)
    df.to_csv("output/film_customers.csv", index=False)
    print("✅ Đã lưu output/film_customers.csv")
    return df

def customers_by_category(conn):
    sql = """
    SELECT 
        cat.name AS category,
        GROUP_CONCAT(DISTINCT CONCAT(c.first_name, ' ', c.last_name) SEPARATOR ', ') AS customers
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category cat ON fc.category_id = cat.category_id
    JOIN customer c ON r.customer_id = c.customer_id
    GROUP BY cat.name
    ORDER BY cat.name;
    """
    df = conn.queryDataset(sql)
    df.to_csv("output/category_customers.csv", index=False)
    print("✅ Đã lưu output/category_customers.csv")
    return df

if __name__ == "__main__":
    conn = Connector()
    customers_by_film(conn)
    customers_by_category(conn)
