import threading

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


@bot.message_handler(commands=['subscribe_test'])
def subscribe_to_test(message):
    name = message.from_user.first_name
    chat_id = message.from_user.id
    if not thread_manager.has_running_elements(chat_id):
        thread_manager.start_thread(chat_id=chat_id,
                                    target=bf.send_message,
                                    args=(bot, chat_id, "Questo è un test"))
        bot.reply_to(message, "Perfetto, "+name+". Da ora riceverai aggiornamenti sulla tua assicurazione")
    else:
        bot.reply_to(message, "Sei già iscritto")


# TODO: Right now there is no way to distinguish between assicurazione thread and test thread.
@bot.message_handler(commands=['unsubscribe_test'])
def unsubscribe_from_test(message):
    chat_id = message.from_user.id
    if thread_manager.has_running_elements(chat_id):
        thread_manager.stop_thread(chat_id=chat_id)
        bot.reply_to(message, "Come vuoi. Da ora non riceverai più aggiornamenti sul test")
    else:
        bot.reply_to(message, "Non sei iscritto")


@bot.message_handler(commands=['subscribe_assicurazione'])
def subscribe_to_assicurazione(message):
    name = message.from_user.first_name
    chat_id = message.from_user.id
    if not thread_manager.has_running_elements(chat_id):
        #threading.Thread(target=send_message, args=(chat_id, "Prova"), daemon=True).start()
        thread_manager.start_thread(chat_id=chat_id,
                                    target=bf.check_assicurazione,
                                    args=(bot, chat_id))
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


def send_message(event: threading.Event, chat_id, message: str):
    while not event.is_set():
        bot.send_message(chat_id=chat_id, text=message)
        time.sleep(5)


# Start the bot polling in a separate thread
bot.infinity_polling()
