from multiprocessing import Process, Array, Value, Manager
from ctypes import c_bool
import time

#This is a Test function simulating the real Analyser
def check_website(finished,data):
    finished.value = False

    #simulate the time it takes for the script to run
    time.sleep(100)

    finished.value = True
    data["abc.at"] = ["test"]



#create a Manager for handeling the communication beteen the Processes and the Server
manager = Manager()

def add_new_Variables(database_dict,url):
    database_dict[url] = {"finished":manager.Value(c_bool,False),"data":manager.dict()}


def spawn_new_Process(database_dict,url):
    finished = database_dict[url]["finished"]
    data = database_dict[url]["data"]
    p1 = Process(target=check_website, args=(finished,data,))
    p1.start()

def check_if_running(database_dict,url):
    return not database_dict[url]["finished"].value

def get_data(database_dict,url):
    return dict(database_dict[url]["data"])
