from threading import Event


class ThreadInstance:

    def __init__(self, thread):
        self.event = Event()
        self.thread = thread

    def start_thread(self):
        while True:
            if self.event.is_set():
                break
            else:
                thread

