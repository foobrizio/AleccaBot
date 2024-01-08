from telebot import TeleBot
from telebot.types import Message

from modules.IMessageHandler import IMessageHandler


class MessageHandler(IMessageHandler):
    @staticmethod
    def desc_mapping():
        return {
            'upload_album': "Upload a new photo collection to your personal cloud",
            'download_album': "Downloads a photo collection from your personal cloud"
        }

    @staticmethod
    def attach_commands(bot: TeleBot):
        bot.register_message_handler(callback=MessageHandler.upload_album,
                                     commands=["upload_album"],
                                     pass_bot=True)
        bot.register_message_handler(callback=MessageHandler.download_album,
                                     commands=["download_album"],
                                     pass_bot=True)

    @staticmethod
    def upload_album(message: Message, bot: TeleBot):
        bot.reply_to(message=message, text="This method is currently in development")

    @staticmethod
    def download_album(message: Message, bot: TeleBot):
        bot.reply_to(message=message, text="This method is currently in development")
