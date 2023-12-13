import os
from telebot import TeleBot
import Consts


class BotFunctions:

    @staticmethod
    def create_new_collection(bot: TeleBot, chat_id: str, collection_name: str):
        user_dir = Consts.root + chat_id + "/"
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        os.makedirs(user_dir+collection_name)

    @staticmethod
    def add_files_to_collection(bot: TeleBot, chat_id: str, collection_name: str, files):
        status = "NOT_YET_IMPLEMENTED"

    @staticmethod
    def get_collection_list(bot: TeleBot, chat_id):
        user_dir = Consts.root + chat_id + "/"
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
            return []
        return [d for d in os.listdir(user_dir) if os.path.isdir(d)]

    @staticmethod
    def send_collection(bot: TeleBot, chat_id: str, collection_name: str):
        user_dir = Consts.root + chat_id + "/"
        collection_dir = user_dir + collection_name
        if not os.path.exists(user_dir):
            bot.send_message(chat_id=chat_id, text="Non hai una collezione di foto")
            return
        elif not os.path.exists(collection_dir):
            bot.send_message(chat_id=chat_id, text="La collezione " + collection_name + " non esiste")
            return
        else:
            bot.send_message(chat_id=chat_id, text="WIP: A breve verrà implementata la possibilità di trasferire questa"
                                                   + " cartella come archivio")
            status = "NOT_YET_IMPLEMENTED"

