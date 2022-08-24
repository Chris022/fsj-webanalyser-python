from bottle import get, run, post, request, response

database = dict()

def analyse_controller(url):
    global database
    #create new variables and add them to the database dict


    #spawn new analyser process

    #return the url as a key to find the results
    return {"type":"SUCCESS","data":url}

def results_controller(url):
    global database
    #start by checking if the analyser process is finished
    if(False):
        return {"type":"ERROR","data":"Still analysing..."}

    #return the data the analyser produced
    return {"type":"SUCCESS","data":{"test":"test"}}

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

