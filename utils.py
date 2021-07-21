import psycopg2 as pg
from telebot import types
import datetime
import calendar
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from prettytable import from_db_cursor
from PIL import Image, ImageDraw, ImageFont
import os

def db_execute(command):
    conn = pg.connect(host='localhost', dbname='di_bot', user='di_bot', password='dipadissdiwd', port='6543')
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(command)
    finally:
        conn.close()


def generate_markup(list):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    # Заполняем разметку перемешанными элементами
    if len(list) % 4 == 0:
        for i in range(0, len(list), 4):
            markup.add(str(list[i]), str(list[i+1]), str(list[i+2]), str(list[i+3]))
    elif len(list) % 3 == 0:
        for i in range(0, len(list), 3):
            markup.add(str(list[i]), str(list[i+1]), str(list[i+2]))
    elif len(list) % 2 == 0:
        for i in range(0, len(list), 2):
            markup.add(str(list[i]), str(list[i+1]))
    else:
        for button in list:
            markup.add(button)
    return markup

def generate_inline(list):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for item in list:
        but = types.InlineKeyboardButton(text = item[0], callback_data=item[1])
        markup.add(but)
    return markup

def generate_img(num):
    conn = pg.connect(host='localhost', dbname='di_bot', user='di_bot', password='dipadissdiwd', port='6543')
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"select * from expences order by load_dttm desc limit {num}")
                mytable = from_db_cursor(cur)
    finally:
        conn.close()

    out = Image.new("RGB", (1900, (110 + 28*num)), color='#272727')

    d = ImageDraw.Draw(out)
    font = ImageFont.truetype("consola.ttf", 32, encoding='UTF-8')

    d.multiline_text((0,0), text=str(mytable), font=font, fill='#ffffff', align='center')
    out.save("tmp.jpg")

def delete_img():
    os.remove("tmp.jpg")



