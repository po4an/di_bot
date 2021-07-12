import psycopg2 as pg

def db_execute(command):
    conn = pg.connect(host='localhost', dbname='di_bot', user='di_bot', password='dipadissdiwd', port='6543')
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(command)
    finally:
        conn.close()