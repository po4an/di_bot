import config
import telebot
import utils
import os



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



@bot.message_handler(content_types= ["text"])
def ahah(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == "__main__":
    bot.polling(none_stop = True)