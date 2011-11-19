from threading import Event, Thread

class StoppableThread(Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()

    def join(self):
        self.stop_soon()
        super(StoppableThread, self).join()

    def stop_soon(self):
        self._stop_event.set()


