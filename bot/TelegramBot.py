import telebot
import Consts
import time

from assicurazione.CheckAssicurazione import CheckAssicurazione
from BotFunctions import BotFunctions as bf
from threads.ThreadManager import ThreadManager

bot = telebot.TeleBot(Consts.bot_token, threaded=False)
thread_manager = ThreadManager()


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    print(message)
    hello_message = "Ciao "+message.from_user.first_name+". Come va?"
    bf.send_message(bot=bot,
                    chat_id=message.from_user.id,
                    message=hello_message)
    #bot.reply_to(message, "Ciao "+message.from_user.first_name+". Come va?")


@bot.message_handler(commands=['subscribe_assicurazione'])
def subscribe_to_assicurazione(message):
    name = message.from_user.first_name
    chat_id = message.from_user.id
    if not thread_manager.has_running_elements(chat_id):
        #threading.Thread(target=send_message, args=(chat_id, "Prova"), daemon=True).start()
        thread_manager.start_thread(chat_id=chat_id,
                                    target=send_message,
                                    args=(chat_id, "Prova"))
        bot.reply_to(message, "Perfetto, "+name+". Da ora riceverai aggiornamenti sulla tua assicurazione")
    else:
        bot.reply_to(message, "Sei già iscritto")


@bot.message_handler(commands=['unsubscribe_assicurazione'])
def unsubscribe_from_assicurazione(message):
    chat_id = message.from_user.id
    if thread_manager.has_running_elements(chat_id):
        thread_manager.stop_thread(chat_id=chat_id)
        bot.reply_to(message, "Come vuoi. Da ora non riceverai più aggiornamenti sulla tua assicurazione")
    else:
        bot.reply_to(message, "Non sei iscritto")


@bot.message_handler(commands=['send_assicurazione'])
def receive_send_command(message):
    chat_id = message.from_user.id
    if not is_subscribed_to_assicurazione(chat_id):
        return
    print(message)
    if CheckAssicurazione.check_da_scaricare():
        bot.reply_to(message, "Sto scaricando il nuovo file assicurazione. Pazienta qualche secondo...")
        CheckAssicurazione.download()
    send_assicurazione(chat_id)


def is_subscribed_to_assicurazione(chat_id):
    return chat_id == 128314363


def send_assicurazione(chat_id):
    file = open(Consts.document, 'rb')
    bot.send_document(chat_id=chat_id,
                      document=file)


def send_message(chat_id, message: str):
    while True:
        bot.send_message(chat_id=chat_id, text=message)
        time.sleep(1)


# Start the bot polling in a separate thread
#bot_thread = threading.Thread(target=bot.infinity_polling())
#bot_thread.start()
bot.infinity_polling()
