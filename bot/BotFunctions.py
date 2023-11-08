import time
from threading import Event

from telebot import TeleBot

import Consts
from assicurazione.CheckAssicurazione import CheckAssicurazione


# How to create a new function?

# 1) Always put event as first parameter.
# 2) Use very short time.sleep period, because an eventual thread.join() will have to wait for the entire time.
#    You can use a cont variable to artificially create a longer delay time between each execution of the
#    function logic.

class BotFunctions:

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
            # We don't need to execute this task very often, since the
            # assicurazione changes once every month.
            # For now, let's put a waiting time of 6 hours, but we should
            # think about a better way to wait for the right time to check
            time.sleep(3600*6)

    @staticmethod
    def send_assicurazione(bot: TeleBot, chat_id):
        file = open(Consts.document, 'rb')
        bot.send_document(chat_id=chat_id,
                          document=file)