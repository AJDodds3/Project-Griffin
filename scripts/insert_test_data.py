from connect import get_connection

def insert_sample_data():
    conn = get_connection()
    cur = conn.cursor()

    # Insert a stock
    cur.execute(
        "INSERT INTO stocks (ticker, company_name) VALUES (%s, %s) RETURNING id;",
        ("AAPL", "Apple Inc.")
    )
    stock_id = cur.fetchone()[0]

    # Insert an author
    cur.execute(
        "INSERT INTO authors (name, organization) VALUES (%s, %s) RETURNING id;",
        ("Jane Doe", "CNBC")
    )
    author_id = cur.fetchone()[0]

    # Insert an article
    cur.execute(
        """
        INSERT INTO articles (title, content, author_id, publish_date, sentiment)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (
            "Apple surprises with strong Q2 earnings",
            "Apple released its Q2 results, surpassing Wall Street expectations with strong iPhone sales.",
            author_id,
            "2025-05-01",
            0.75  # Sentiment score
        )
    )
    article_id = cur.fetchone()[0]

    # Link article to stock
    cur.execute(
        "INSERT INTO article_stock_link (article_id, stock_id) VALUES (%s, %s);",
        (article_id, stock_id)
    )

    conn.commit()
    conn.close()
    print("Test data inserted successfully.")

if __name__ == "__main__":
    insert_sample_data()
