from telebot import TeleBot


class IMessageHandler:

    @staticmethod
    def desc_mapping():
        """ This method should be implemented in order to create a mapping between each bot
            command and the relative description
        """
        pass

    @staticmethod
    def attach_commands(bot: TeleBot):
        """ This method should be implemented in order to register message handlers for the bot
            and associate them to specific commands
        """
        pass
