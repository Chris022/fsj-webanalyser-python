from bottle import get, run, post, request, response, static_file, route
from concurrency_controller import add_new_variables, spawn_new_process, check_if_running, get_data,check_visited_pages
from analyse_controller import analyse_url
from view_controller import view_main,view_results


database = dict()

def analyse_controller(url):
    global database
    #create new variables and add them to the database dict
    add_new_variables(database,url)

    #spawn new analyser process
    spawn_new_process(database,url,analyse_url(url,))

    #return the url as a key to find the results
    return {"type":"SUCCESS","data":url}

def results_controller(url):
    global database
    #start by checking if the url was already analysed
    if(not url in database.keys()):
        return {"type":"ERROR","data":"not_analysed","message":"You have to analyse a url before you can see the Results"}
    #start by checking if the analyser process is finished
    if(check_if_running(database,url)):
        visited_pages = check_visited_pages(database,url)
        #return view_results_not_finished(visited_pages)
        return {"type":"ERROR","data":"still_analysing","info_data":{"visited_pages":visited_pages},"message":"Still analysing...This might take multiple hours!Be patient!"}

    #return the data the analyser produced
    return {"type":"SUCCESS","data":get_data(database,url)}

@get('/')
def index():
    return static_file("index.html", root='public')

@route('/<filename>')
def send_static(filename):
    return static_file(filename, root='public')

@route('/js/<filename>')
def send_static(filename):
    return static_file(filename, root='public/js')

@post('/analyse')
def analyse():
    #return json
    response.set_header('Content-Type', 'application/json')
    #validate input
    input_data = request.json
    if(not "url" in input_data.keys()):
        return {"type":"ERROR","data":"invalid_input","message":"Invalid input data: {url:<value>} is required"}
    #handle request
    return analyse_controller(input_data["url"])

@post('/results')
def results():
    #return json
    response.set_header('Content-Type', 'application/json')
    #validate input
    input_data = request.json
    if(not "url" in input_data.keys()):
        return {"type":"ERROR","data":"invalid_input","message":"Invalid input data: {url:<value>} is required"}
    #handle request
    return results_controller(input_data["url"])


run(host='0.0.0.0', port=8080)

