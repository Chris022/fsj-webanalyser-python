from multiprocessing import Process, Array, Value, Manager
from ctypes import c_bool
import time

def analyse_website(finished,data,analyse_function):
    finished.value = False

    #analyse the url
    list_of_visited_urls,analyse_results = analyse_function()

    finished.value = True
    data["list_of_visited_urls"] = list_of_visited_urls
    data["analyse_results"] = analyse_results



#create a Manager for handeling the communication beteen the Processes and the Server
manager = Manager()

def add_new_variables(database_dict,url):
    database_dict[url] = {"finished":manager.Value(c_bool,False),"data":manager.dict()}


def spawn_new_process(database_dict,url,analyse_function):
    #prep variables
    finished = database_dict[url]["finished"]
    data = database_dict[url]["data"]
    #prep analyse function
    analyse_function_preped = lambda: analyse_function(url)
    p1 = Process(target=analyse_website, args=(finished,data,analyse_function_preped,))
    p1.start()

def check_if_running(database_dict,url):
    return not database_dict[url]["finished"].value

def get_data(database_dict,url):
    return dict(database_dict[url]["data"])
