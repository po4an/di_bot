import psycopg2 as pg
from prettytable import from_db_cursor
from PIL import Image, ImageDraw, ImageFont
import os
"""connection = pg.connect("mydb.db")
cursor.execute("SELECT field1, field2, field3 FROM my_table")
mytable = from_db_cursor(cursor)"""
"""conn = pg.connect(host='localhost', dbname='di_bot', user='di_bot', password='dipadissdiwd', port='6543')
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("select * from expences order by load_dttm desc limit 5")
            mytable = from_db_cursor(cur)
finally:
    conn.close()


out = Image.new("RGB", (1770,268), color='#272727')

d = ImageDraw.Draw(out)
font = ImageFont.truetype("consola.ttf", 32, encoding='UTF-8')

d.multiline_text((20,20), text = str(mytable),font=font, fill='#ffffff', align='center')
out.show()
out.save("tmp.jpg")"""
#os.remove("tmp.jpg")
list = [3,5,10,15,30,50]
for i in range(0,len(list),3):
    print(list[i], list[i+1], list[i+2])
