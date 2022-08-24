from bottle import get, run, post, request, response
from concurrency_controller import add_new_variables, spawn_new_process, check_if_running, get_data
from analyse_controller import analyse_url


database = dict()

def analyse_controller(url):
    global database
    #create new variables and add them to the database dict
    add_new_variables(database,url)

    #spawn new analyser process
    spawn_new_process(database,url,analyse_url)

    #return the url as a key to find the results
    return {"type":"SUCCESS","data":url}

def results_controller(url):
    global database
    #start by checking if the analyser process is finished
    if(check_if_running(database,url)):
        return {"type":"ERROR","data":"Still analysing..."}

    #return the data the analyser produced
    return {"type":"SUCCESS","data":get_data(database,url)}

@get('/')
def index():
    return "This is the API for the fjs-webanalyser"

@post('/analyse')
def analyse():
    #return json
    response.set_header('Content-Type', 'application/json')
    #validate input
    input_data = request.json
    if(not "url" in input_data.keys()):
        return {"type":"ERROR","data":"Invalid input data: {url:<value>} is required"}
    #handle request
    return analyse_controller(input_data["url"])

@post('/results')
def results():
    #return json
    response.set_header('Content-Type', 'application/json')
    #validate input
    input_data = request.json
    if(not "url" in input_data.keys()):
        return {"type":"ERROR","data":"Invalid input data: {url:<value>} is required"}
    #handle request
    return results_controller(input_data["url"])


run(host='localhost', port=8080)

