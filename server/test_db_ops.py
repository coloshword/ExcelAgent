## test_db_ops: testing sample database operations 
import psycopg2

def test_postgres_conn():
    conn = psycopg2.connect(
        database = "test_db",
        host="localhost",
        password="2001",
        port=5432
    )
    cur = conn.cursor()
    sample_query = """
    SELECT * from weather
    """
    cur.execute(sample_query)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.commit()
    cur.close()
    conn.close()
if __name__ == "__main__":
    test_postgres_conn()