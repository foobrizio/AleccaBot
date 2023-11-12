import threading


class SubscriptionManager:

    def __init__(self):
        self.threads_dict = {}

    def is_subscribed(self, chat_id, subscription_name: str):
        if not self.has_running_elements(chat_id):
            return False
        thread_list = self.threads_dict[chat_id]
        print(thread_list)
        for thread_elem in thread_list:
            if thread_elem[0] == subscription_name:
                return True
        return False

    def has_running_elements(self, chat_id):
        try:
            thread_list = self.threads_dict[chat_id]
            return True
        except (KeyError, IndexError) as error:
            return False

    def get_running_elements(self, chat_id):
        try:
            return self.threads_dict[chat_id]
        except KeyError:
            return []

    # N.B: A target function should always have an Event object inside,
    # in order to safely terminate the thread.
    def start_thread(self, name: str, chat_id, target, **args):
        event = threading.Event()
        args['args'] = (event,) + args['args']
        new_thread = threading.Thread(target=target,
                                      daemon=True,
                                      **args)
        try:
            existing_data = self.threads_dict[chat_id]
            existing_data.append((name, new_thread, event))
            self.threads_dict[chat_id] = existing_data
        except KeyError:
            self.threads_dict[chat_id] = [(name, new_thread, event)]
        new_thread.start()

    def stop_thread(self, chat_id, thread_name: str):
        try:
            thread_list = self.threads_dict[chat_id]
            target_index = 0
            for x in range(len(thread_list)):
                if thread_list[x][0] == thread_name:
                    target_index = x

            event: threading.Event = thread_list[x][2]
            thread: threading.Thread = thread_list[x][1]
            event.set()
            thread.join()
            thread_list.pop(x)
            self.threads_dict[chat_id] = thread_list
            print(self.threads_dict)
        except KeyError:
            print("Nessun thread per l'utente con id %id" % chat_id)
