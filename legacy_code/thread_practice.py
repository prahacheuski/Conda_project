from multiprocessing import Process, freeze_support
from time import sleep


def f():
    print("AAaaa....")
    sleep(30)


if __name__ == '__main__':
    freeze_support()
    Process(target=f).start()
