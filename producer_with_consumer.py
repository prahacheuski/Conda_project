from threading import *
from time import sleep

cookies = 0


def producer():
    cur_thread = current_thread().name
    global cookies
    while True:
        cookies += 1
        print("{} made a cookie, left {}".format(cur_thread, cookies))
        sleep(4)


def consumer():
    cur_thread = current_thread().name
    global cookies
    while True:
        if cookies:
            print("{} munching a cookie".format(cur_thread))
            cookies -= 1
        else:
            print("No cookie :(")
            sleep(15)


t1 = Thread(target=producer, name="Producer")
t2 = Thread(target=consumer, name="Consumer")
t1.start()
t2.start()
