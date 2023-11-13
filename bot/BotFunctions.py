import time
from threading import Event

from telebot import *

import Consts
from assicurazione.CheckAssicurazione import CheckAssicurazione


# How to create a new function?

# 1) Always put event as first parameter.
# 2) Use very short time.sleep period, because an eventual thread.join() will have to wait for the entire time.
#    You can use a cont variable to artificially create a longer delay time between each execution of the
#    function logic.

class BotFunctions:

    @staticmethod
    def set_default_commands(bot: TeleBot):
        bot.set_my_commands([
            telebot.types.BotCommand("/hello", "Sends a welcome message"),
            telebot.types.BotCommand("/subscribe_test", "Activate the test thread. Just for didactic purpose"),
            telebot.types.BotCommand("/subscribe_assicurazione", "Activate the assicurazione thread. "),
            telebot.types.BotCommand("/unsubscribe", "Unsubscribes from an active subscription")
        ])

    @staticmethod
    def send_message(event: Event, bot: TeleBot,  chat_id, message: str):
        cont = 0
        while not event.is_set():
            if cont == 4:
                bot.send_message(chat_id=chat_id, text=message)
                cont = 0
            time.sleep(1)
            cont = cont+1

    @staticmethod
    def check_assicurazione(event: Event, bot: TeleBot, chat_id):
        cont = 0
        while not event.is_set():
            if cont == 3600*6:
                if CheckAssicurazione.check_da_scaricare():
                    CheckAssicurazione.download()
                    BotFunctions.send_assicurazione(bot, chat_id)
                cont = 0
            time.sleep(1)
            cont = cont+1

    @staticmethod
    def send_assicurazione(bot: TeleBot, chat_id):
        file = open(Consts.document, 'rb')
        bot.send_document(chat_id=chat_id,
                          document=file)
