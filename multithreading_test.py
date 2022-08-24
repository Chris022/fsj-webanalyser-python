from multiprocessing import Process, Array, Value, Manager
from ctypes import c_bool, c_wchar_p
import time

def check_website(finished,data):
    finished.value = False

    #simulate the time it takes for the script to run
    time.sleep(1)

    finished.value = True
    data["abc.at"] = ["test"]

manager = Manager()

finished1 = manager.Value(c_bool,False)
data1 = manager.dict()

finished2 = manager.Value(c_bool,False)
data2 = manager.dict()


p1 = Process(target=check_website, args=(finished1,data1,))
p1.start()
p2 = Process(target=check_website, args=(finished2,data2,))
p2.start()

while True:
    print("Thread 1: " + str(finished1.value))
    print("Thread 1: " + str(data1))
    print("Thread 2: " + str(finished2.value))