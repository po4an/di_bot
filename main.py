import config
import telebot
from telebot import types
from utils import db_execute, generate_markup, generate_img, delete_img, generate_inline
import os
import psycopg2 as pg
import datetime
from prettytable import from_db_cursor



bot = telebot.TeleBot(config.token)
expence_types = ["Табак", "HQD", "IZI", "Аксуссуары", "Личные расходы", "Зарплаты", "Для знакомых", "Другое"]
common_count_rows = [3,5,10,15,30,50]


@bot.message_handler(commands = ["start"])
def hello(message):
    sti = open("stics/hello.webp", "rb")
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Доброе время суток, товарищ {}.\n"
                                      "Я помогу тебе в ведении расходов.\n"
                                      "Нажимай кнопку 'Команды' и посмотри, что я могу".format(message.from_user.first_name), reply_markup=generate_markup(["Команды"]))

@bot.message_handler(regexp="Команды")
def handle_message(message):
    bot.send_message(message.chat.id, "Что хочешь сделать?", reply_markup=generate_markup(["/add_expence", "/sum_expences", "/last_5_rows", "/last_rows", "/delete_rows"]))


"""@bot.message_handler(commands=["commands"])
def info(message):
    bot.send_message(message.chat.id, "Команды, которые у меня есть:\n"
                                      "/commands - узнать мои команды\n"
                                      "/add_expence - внести расходы\n"
                                      "/sum_expences - узнать сумму всех расходов\n"
                                      "/last_5_rows - показать 5 последних расходов\n"
                                      "/last_rows - показать определенное количество последних операций\n"
                                      "/delete_rows - удалить записи по их id")"""

"""@bot.message_handler(content_types= ["text"])
def ahah(message):
    bot.send_message(message.chat.id, message.text)"""


@bot.message_handler(commands=['add_expence'])
def add_expence(message):
    bot.reply_to(message=message, text = 'Жми, если захочешь отменить операцию', reply_markup=generate_inline([("отмена операции", "stop_operation")]))
    send = bot.send_message(message.chat.id, 'Внеси количество денег, которые потратил', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(send, add_desc)


def add_desc(message):
    global temp
    try:
        msg_val = int(message.text.lower())
        try:
            temp = [message.from_user.first_name + " " + message.from_user.last_name, msg_val]
        except:
            temp = [message.from_user.first_name , msg_val]
        send = bot.send_message(message.chat.id, 'На что пошел расход?\nКраткое описание')
        print(temp)
        bot.register_next_step_handler(send, add_expence_type)
    except:
        send = bot.send_message(message.chat.id, 'Это не число, введи число')
        bot.register_next_step_handler(send, add_desc)

def add_expence_type(message):
    global temp
    temp.append(message.text.lower())
    send = bot.send_message(message.chat.id, "У расхода есть какой то тип?", reply_markup=generate_markup(expence_types))
    bot.register_next_step_handler(send, expence_generate)

def expence_generate(message):
    global temp
    text = message.text.lower()
    if text not in expence_types:
        text = "другое"
    temp.append(text)
    print(temp)
    db_execute(f"insert into expences (user_name, expence, description, expence_type) values ( '{temp[0]}', {temp[1]}, '{temp[2]}', '{temp[3]}')")
    bot.send_message(message.chat.id, "Успешно!\nТвоя запись в базе", reply_markup=generate_markup(["Команды"]))


@bot.message_handler(commands=["sum_expences"])
def sum_expences_step1(message):
    send = bot.send_message(message.chat.id, "За какую дату хотел бы посмотреть расходы?", reply_markup=generate_markup(["Текущий день", "Текущая неделя", "Текущий месяц", "Текущий год"]))
    bot.register_next_step_handler(send, sum_expence_step2)

def sum_expence_step2(message):
    answer = message.text.lower()
    if answer == "текущий день":
        conn = pg.connect(host='postgres', dbname='di_bot', user='di_bot', password='dipadissdiwd', port='5432')
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("select sum(expence) from expences where load_dttm::date = current_date")
                    sum_expences = cur.fetchone()[0]
        finally:
            conn.close()

        bot.send_message(message.chat.id, f"Сумма трат за текущий день: {sum_expences}", reply_markup=generate_markup(["Команды"]))
    if answer == "текущая неделя":
        conn = pg.connect(host='postgres', dbname='di_bot', user='di_bot', password='dipadissdiwd', port='5432')
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("select sum(expence) from expences where extract(week from load_dttm) = extract(week from current_date) and extract(year from load_dttm) = extract(year from current_date)")
                    sum_expences = cur.fetchone()[0]
        finally:
            conn.close()

        bot.send_message(message.chat.id, f"Сумма трат за текущую неделю: {sum_expences}", reply_markup=generate_markup(["Команды"]))
    if answer == "текущий месяц":
        conn = pg.connect(host='postgres', dbname='di_bot', user='di_bot', password='dipadissdiwd', port='5432')
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("select sum(expence) from expences where extract(month from load_dttm) = extract(month from current_date) and extract(year from load_dttm) = extract(year from current_date)")
                    sum_expences = cur.fetchone()[0]
        finally:
            conn.close()

        bot.send_message(message.chat.id, f"Сумма трат за текущий месяц: {sum_expences}", reply_markup=generate_markup(["Команды"]))
    if answer == "текущий год":
        conn = pg.connect(host='postgres', dbname='di_bot', user='di_bot', password='dipadissdiwd', port='5432')
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("select sum(expence) from expences where extract(year from load_dttm) = extract(year from current_date)")
                    sum_expences = cur.fetchone()[0]
        finally:
            conn.close()
        bot.send_message(message.chat.id, f"Сумма трат за текущий год: {sum_expences}", reply_markup=generate_markup(["Команды"]))

@bot.message_handler(commands=['last_5_rows'])
def last(message):
    generate_img(5)
    with open('tmp.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, reply_markup=generate_markup(["Команды"]))
    delete_img()

@bot.message_handler(commands=['last_rows'])
def count_rows(message):
    bot.reply_to(message=message, text = 'Жми, если захочешь отменить операцию', reply_markup=generate_inline([("отмена операции", "stop_operation")]))
    markup = generate_markup(common_count_rows)
    send = bot.send_message(message.chat.id, "Сколько последних операций хотели бы видеть?", reply_markup=markup)
    bot.register_next_step_handler(send, fetch_rows)

def fetch_rows(message):

    try:
        count = int(message.text.lower())
        generate_img(count)
        with open('tmp.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=generate_markup(["Команды"]))
        delete_img()
    except:
        send = bot.send_message(message.chat.id, "Мне нужно число")
        bot.register_next_step_handler(send, fetch_rows)


@bot.message_handler(commands=['delete_rows'])
def rows_id(message):
    bot.reply_to(message=message, text = 'Жми, если захочешь отменить операцию', reply_markup=generate_inline([("отмена операции", "stop_operation")]))
    send = bot.send_message(message.chat.id, "Введи номера строк через пробел, которые хотел бы удалить", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(send, parse_rows_id)
def parse_rows_id(message):
    try:
        text = message.text.lower()
        rows_list = [int(id) for id in text.split(" ")]
        for id in rows_list:
            db_execute(f"insert into expences_del select * from expences where id = {id};"
                       f"delete from expences where id = {id};"
                       f"insert into expences_del_history (row_id, user_name) values ({id}, '{message.from_user.first_name} {message.from_user.last_name}')")
        bot.send_message(message.chat.id, "Успешно, записи удалены", reply_markup=generate_markup(["Команды"]))
    except:
        send = bot.send_message(message.chat.id, "Введи корректные id записей, которые есть в базе, через пробел")
        bot.register_next_step_handler(send, parse_rows_id)




@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == "stop_operation":
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, "Операция отменена", reply_markup=generate_markup(["Команды"]))


if __name__ == "__main__":
    bot.polling(none_stop = True)