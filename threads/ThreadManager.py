import threading



class ThreadManager:

    def __init__(self):
        self.threads_dict = {}

    def has_running_elements(self, chat_id):
        try:
            elem = self.threads_dict[chat_id]
            return True
        except KeyError:
            return False

    # N.B: A target function should always have an Event object inside,
    # in order to safely terminate the thread.
    def start_thread(self, chat_id, target, **args):
        event = threading.Event()
        args['args'] = (event,) + args['args']
        new_thread = threading.Thread(target=target,
                                      daemon=True,
                                      **args)
        self.threads_dict[chat_id] = (new_thread, event)
        new_thread.start()

    def stop_thread(self, chat_id):
        try:
            event: threading.Event = self.threads_dict[chat_id][1]
            thread: threading.Thread = self.threads_dict[chat_id][0]
            event.set()
            thread.join()
            del self.threads_dict[chat_id]
        except KeyError:
            print("Nessun thread per l'utente con id %id" % chat_id)
