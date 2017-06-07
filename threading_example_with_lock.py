import threading
from time import sleep


class Waiter(threading.Thread):
    def __init__(self):
        super(Waiter, self).__init__()
        self.setDaemon(False)

    def work(self):
        print("Started work")
        sleep(5)
        print("Work completed")

    def run(self):
        self.work()


w = Waiter()
w.start()
