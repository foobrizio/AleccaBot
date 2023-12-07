import time
from threading import Event

from telebot import TeleBot

import Consts
from modules.assicurazione.CheckAssicurazione import CheckAssicurazione


class BotFunctions:
    # Intervallo in secondi per ogni controllo
    interval = 3600 * 6

    @staticmethod
    def check_assicurazione(event: Event, bot: TeleBot, chat_id):

        # Alla prima iterazione facciamo subito un check
        cont = BotFunctions.interval
        while not event.is_set():
            if cont == BotFunctions.interval:
                if CheckAssicurazione.check_da_scaricare():
                    CheckAssicurazione.download()
                    BotFunctions.send_assicurazione(bot, chat_id)
                cont = 0
            time.sleep(1)
            cont = cont + 1

    @staticmethod
    def send_assicurazione(bot: TeleBot, chat_id):
        file = open(Consts.document, 'rb')
        bot.send_document(chat_id=chat_id,
                          document=file)
