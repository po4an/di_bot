import config
import telebot
from utils import db_execute
import os
import psycopg2 as pg



bot = telebot.TeleBot(config.token)



"""@bot.message_handler(commands = ["test"])
def tete(message):
    for i in os.listdir("musmp3/"):
        if i.split(".")[-1] == "ogg":
            f = open('musmp3/' + i, 'rb')
            ty = bot.send_voice(message.chat.id, f)
            bot.send_message(message.chat.id, ty.voice.file_id, reply_to_message_id = ty.message_id)"""


"""@bot.message_handler(commands = ["game"])
def game(message):
    db_worker = SQLighter(config.database_name)
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    markup = utils.generate_markup(row[0][2], row[0][3])
    bot.send_voice(message.chat.id, row[0][1], reply_markup = markup)
    utils.set_user_game(message.chat.id, row[0][2])
    db_worker.close()"""

@bot.message_handler(commands = ["start"])
def hello(message):
#    sti = open("stic/hello.webp", "rb")
#    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Доброе время суток, товарищ {}.\n"
                                      "Я помогу тебе в ведении бизнеса\n"
                                      "Нажми команду /info и посмотри, что я могу".format(message.from_user.first_name))
@bot.message_handler(commands=["info"])
def info(message):
    bot.send_message(message.chat.id, "Команды, которые у меня есть:\n"
                                      "/info - узнать мои команды\n"
                                      "/costs - внести расходы\n"
                                      "/sum_costs - узнать сумму всех расходов")

"""@bot.message_handler(content_types= ["text"])
def ahah(message):
    bot.send_message(message.chat.id, message.text)"""


@bot.message_handler(commands=['costs'])
def to_incure_cost(message):
    send = bot.send_message(message.chat.id, 'Внеси количество денег, сколько ты потратил')
    bot.register_next_step_handler(send, to_incure_desc)



def to_incure_desc(message):
    global temp
    try:
        msg_val = int(message.text.lower())
        temp = [message.from_user.first_name + " " + message.from_user.last_name, msg_val]
        send = bot.send_message(message.chat.id, 'Введи то, на что ты потратил деньги')
        print(temp)
        bot.register_next_step_handler(send, costs_generate)
    except:
        send = bot.send_message(message.chat.id, 'Это не число, введи число')
        bot.register_next_step_handler(send, to_incure_desc)

def costs_generate(message):
    global temp
    temp.append(message.text.lower())
    print(temp)
    db_execute(f"insert into costs (user_name, cost, description) values ( '{temp[0]}', {temp[1]}, '{temp[2]}')")
    bot.send_message(message.chat.id, "Успешно!\nТвоя запись в базе")


@bot.message_handler(commands=["sum_costs"])
def sum_costs(message):
    conn = pg.connect(host='localhost', dbname='di_bot', user='di_bot', password='dipadissdiwd', port='6543')
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("select sum(cost) from costs")
                sum_costs = cur.fetchone()[0]
    finally:
        conn.close()

#добавить время добавления записи
    send = bot.send_message(message.chat.id, f"Сумма трат : {sum_costs}")

if __name__ == "__main__":
    bot.polling(none_stop = True)