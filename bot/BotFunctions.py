from threading import Event

from telebot import *

from modules.ModuleHandler import ModuleHandler

# How to create a new function?

# 1) Always put event as first parameter.
# 2) Use very short time.sleep period, because an eventual thread.join() will have to wait for the entire time.
#    You can use a cont variable to artificially create a longer delay time between each execution of the
#    function logic.


class BotFunctions:

    def __init__(self):
        self.module_commands = {}

    @staticmethod
    def get_default_commands():
        return [
            telebot.types.BotCommand("/hello", "Sends a welcome message"),
            telebot.types.BotCommand("/unsubscribe", "Unsubscribes from an active subscription"),
            telebot.types.BotCommand("/subscribe_test", "Activate the test thread. Just for didactic purpose"),
        ]

    # @staticmethod
    # def set_default_commands(bot: TeleBot):
    #     bot.set_my_commands([
    #         telebot.types.BotCommand("/hello", "Sends a welcome message"),
    #         telebot.types.BotCommand("/unsubscribe", "Unsubscribes from an active subscription"),
    #         telebot.types.BotCommand("/subscribe_test", "Activate the test thread. Just for didactic purpose"),
    #         # # ASSICURAZIONE
    #         # telebot.types.BotCommand("/subscribe_assicurazione", "Activate the assicurazione thread. "),
    #         # # CLOUD
    #         # telebot.types.BotCommand("/upload_album", "Uploads a new photo collection to your personal cloud"),
    #         # telebot.types.BotCommand("/download_album", "Downloads a photo collection from your personal cloud")
    #     ])

    @staticmethod
    def update_commands(bot: TeleBot):
        mh = ModuleHandler()
        module_commands = mh.discover_commands()
        command_list = BotFunctions.get_default_commands()
        for command in module_commands.keys():
            command_list.append(telebot.types.BotCommand("/"+command, module_commands[command]))
        bot.set_my_commands(command_list)
        mh.load_modules(bot=bot)

    @staticmethod
    def send_message(event: Event, bot: TeleBot,  chat_id, message: str):
        cont = 0
        if event is not None:
            while not event.is_set():
                if cont == 4:
                    bot.send_message(chat_id=chat_id, text=message)
                    cont = 0
                time.sleep(1)
                cont = cont+1
        else:
            bot.send_message(chat_id=chat_id, text=message)
