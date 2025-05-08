from connect import get_connection

def test_connection():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        print("Connected to Supabase at: ", result[0])
        conn.close()
    except Exception as e:
        print("Connection failed: ", e)

if __name__ == "__main__":
    test_connection()
