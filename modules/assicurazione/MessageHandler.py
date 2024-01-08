
from telebot import TeleBot
from telebot.types import Message

from bot.SubscriptionManager import SubscriptionManager
from modules.assicurazione.Functions import Functions as funcs
from modules.IMessageHandler import IMessageHandler


class MessageHandler(IMessageHandler):

    @staticmethod
    def desc_mapping():
        return {
            'subscribe_assicurazione': "Activate the assicurazione thread. ",
        }

    @staticmethod
    def attach_commands(bot: TeleBot):
        bot.register_message_handler(callback=MessageHandler.subscribe_to_assicurazione,
                                     commands=["subscribe_assicurazione"],
                                     pass_bot=True)

    @staticmethod
    def subscribe_to_assicurazione(message: Message, sub_mgr: SubscriptionManager, bot: TeleBot):
        subscription_name = "Assicurazione"
        name = message.from_user.first_name
        chat_id = message.from_user.id
        if not sub_mgr.is_subscribed(chat_id, subscription_name):
            sub_mgr.start_thread(chat_id=chat_id,
                                 name=subscription_name,
                                 target=funcs.check_assicurazione,
                                 args=(bot, chat_id))
            bot.reply_to(message, "Perfetto, "+name+". Da ora riceverai aggiornamenti su "+subscription_name)
        else:
            bot.reply_to(message, "Sei già iscritto")
