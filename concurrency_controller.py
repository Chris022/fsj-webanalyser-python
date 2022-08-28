from multiprocessing import Process, Array, Value, Manager
from ctypes import c_bool,c_int
import time

def analyse_website(finished,number_of_visited_pages,data,analyse_function):
    finished.value = False
    number_of_visited_pages.value = 0

    #analyse the url
    list_of_visited_urls,analyse_results = analyse_function(number_of_visited_pages)

    finished.value = True
    data["list_of_visited_urls"] = list_of_visited_urls
    data["analyse_results"] = analyse_results



#create a Manager for handeling the communication beteen the Processes and the Server
manager = Manager()

def add_new_variables(database_dict,url):
    database_dict[url] = {"finished":manager.Value(c_bool,False),"number_of_visited_pages":manager.Value(c_int,0),"data":manager.dict()}


def spawn_new_process(database_dict,url,analyse_function):
    #prep variables
    finished = database_dict[url]["finished"]
    number_of_visited_pages = database_dict[url]["number_of_visited_pages"]
    data = database_dict[url]["data"]
    #prep analyse function
    analyse_function_preped = analyse_function(url)
    p1 = Process(target=analyse_website, args=(finished,number_of_visited_pages,data,analyse_function_preped,))
    p1.start()

def check_if_running(database_dict,url):
    return not database_dict[url]["finished"].value

def check_visited_pages(database_dict,url):
    return database_dict[url]["number_of_visited_pages"].value

def get_data(database_dict,url):
    return dict(database_dict[url]["data"])
