from time import sleep
from threading import Thread, Semaphore


def nowait(val):
    s = Semaphore(val)

    def higher_wrapper(func):
        def wrapper(some_string):
            t = Thread(target=func, args=(some_string, s))
            t.start()

        return wrapper

    return higher_wrapper


@nowait(2)
def worker(sec, *args):
    with args[0]:
        print("Started work")
        sleep(sec)
        print("Work completed")


worker(5)
worker(5)
worker(5)
worker(5)
