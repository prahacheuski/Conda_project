import threading
import time

global_num = 0

l = threading.Lock()


def parallel_cod(*args, **kwargs):
    current_thread = threading.current_thread().name
    if not current_thread.endswith("1"):
        # l.acquire()
        with l:
            print("parallel cod started in {}".format(current_thread))
            time.sleep(1)
        global global_num
        global_num += args[0]
        print("parallel cod is completed in {}".format(current_thread))
        # l.release()


threads = []
for _ in range(898):
    threads.append(threading.Thread(target=parallel_cod, daemon=True, args=(_,), kwargs={"key": "value"}))

print("main code is running")

for t in threads:
    t.start()

time.sleep(1000)
print("main code is complete and global num = {}".format(global_num))
