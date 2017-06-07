from threading import *
from time import sleep
from random import uniform

cookies = 0
e = Event()


def producer():
    cur_thread = current_thread().name
    global cookies
    while True:
        cookies += 1
        e.set()
        uni = round(uniform(6, 9), 1)
        print("{} made a cookie, next cookie in {} sec".format(cur_thread, uni))
        sleep(uni)


def consumer():
    cur_thread = current_thread().name
    global cookies
    while True:
        e.wait()
        cookies -= 1
        print("{} munching a cookie".format(cur_thread))
        e.clear()


t1 = Thread(target=producer, name="Producer")
t2 = Thread(target=consumer, name="Consumer")
t1.start()
t2.start()
