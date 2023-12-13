import os


class ModuleHandler:

    @staticmethod
    def discover_modules():
        modules_dir = './'
        return [d for d in os.listdir(modules_dir) if os.path.isdir(d) and os.path.isfile(d+"MessageHandler.py")]

    def discover_commands(self):
        module_dirs = self.discover_modules()
        command_list = []


