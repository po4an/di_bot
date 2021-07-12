import psycopg2 as pg

con = pg.connect(host = 'localhost', dbname = 'di_bot', user = 'di_bot', password = 'dipadissdiwd', port = '6543')
cur = con.cursor()
cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, " +
    "login VARCHAR(64), password VARCHAR(64))")
con.commit()

conn = pg.connect(host = 'localhost', dbname = 'di_bot', user = 'di_bot', password = 'dipadissdiwd', port = '6543')
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("select avg(password) from users")
            print(cur.fetchall())
finally:
    conn.close()