import threading

from ThreadInstance import ThreadInstance


class ThreadManager:

    def __init__(self):
        self.threads_dict = {}

    def has_running_elements(self, chat_id):
        try:
            elem = self.threads_dict[chat_id]
            return True
        except KeyError:
            return False

    def start_thread(self, chat_id, target, **args):
        new_thread = threading.Thread(target=target,
                                      daemon=True,
                                      **args)
        self.threads_dict[chat_id] = ThreadInstance(new_thread)
        new_thread.start()

    def stop_thread(self, chat_id):
        try:
            thread_instance = self.threads_dict[chat_id]
            thread_instance.stop()
        except KeyError:
            print("Nessun thread per l'utente con id %id" % chat_id)
