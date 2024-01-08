import importlib
import os

from telebot import TeleBot


class ModuleHandler:
    modules_dir = 'modules'

    def discover_modules(self):
        modules_dir_path = "../"+self.modules_dir+"/"
        return [d for d in os.listdir(modules_dir_path) if
                os.path.isdir(modules_dir_path + d) and os.path.isfile(modules_dir_path + d + "/MessageHandler.py")]

    def discover_commands(self):
        module_dirs = self.discover_modules()
        command_list = {}
        for mod_dir in module_dirs:
            module = importlib.import_module("modules."+mod_dir+".MessageHandler")
            commands = module.MessageHandler.desc_mapping()
            command_list.update(commands)
        return command_list

    def load_modules(self, bot: TeleBot):
        module_dirs = self.discover_modules()
        for mod_dir in module_dirs:
            module = importlib.import_module("modules." + mod_dir + ".MessageHandler")
            module.MessageHandler.attach_commands(bot=bot)
