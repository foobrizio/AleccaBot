from telebot import TeleBot

from modules.IMessageHandler import IMessageHandler


class MessageHandler(IMessageHandler):
    @staticmethod
    def mapping():
        return {
            'upload_album': 'upload_album',
            'download_album': 'download_album'
        }

    @staticmethod
    def upload_album(bot: TeleBot, message):
        bot.reply_to(message=message, text="This method is currently in development")

    @staticmethod
    def download_album(bot: TeleBot, message):
        bot.reply_to(message=message, text="This method is currently in development")