import time
from threading import Event

from telebot import TeleBot

from modules.assicurazione import Consts
from modules.assicurazione.CheckAssicurazione import CheckAssicurazione


class Functions:

    @staticmethod
    def check_assicurazione(event: Event, bot: TeleBot, chat_id):
        cont = 0
        while not event.is_set():
            if cont == 3600 * 6:
                if CheckAssicurazione.check_da_scaricare():
                    CheckAssicurazione.download()
                    Functions.send_assicurazione(bot, chat_id)
                cont = 0
            time.sleep(1)
            cont = cont + 1

    @staticmethod
    def send_assicurazione(bot: TeleBot, chat_id):
        file = open(Consts.document, 'rb')
        bot.send_document(chat_id=chat_id,
                          document=file)
