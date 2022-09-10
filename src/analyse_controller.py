from selenium_connector import SeleniumConnector
#from ghost_py_connector import GhostPyConnector
import time
import re

def check_thrid_party_requets(driver,domain_url):
    thrid_party_calls = []
    for request_url in driver.getThirdPartyRequets():
        #check if url is from a thrid party
        if(not re.match("^http(s)?://"+"(.+\.)?"+domain_url,request_url)):
            #remove slash and just use adress
            request_url = request_url.replace("https://","")
            request_url = request_url.replace("http://","")
            request_url = request_url.split("/")[0]
            thrid_party_calls.append(request_url)
    driver.clearRequets()
    #remove list without doubles
    return list(dict.fromkeys(thrid_party_calls))

def check_cookies(driver):
    cookies = driver.getCookies()
    return cookies

def crawl_links(result_dict,driver,domain_url,list_of_visited_urls,number_of_visited_pages,url):

    #check if url was already visited
    if(url in list_of_visited_urls):
        return

    #check if number of visited pages is bigger than 20
    if(number_of_visited_pages.value > 20):
        return

    #get page content
    #print("Visiting: "+"https://+domain_url+"/"+url)
    driver.open("https://"+domain_url+"/"+url)

    #increase the counter for the number of visited pages
    number_of_visited_pages.value += 1;


    #do checks on webpage
    #check thrid party requets
    #check cookies
    #store result in a result dict if array is not empty
    #dict structure: {url:{third-party-requests:[],cookies:[]}}
    thrid_party_calls = []
    cookies = []
    thrid_party_calls = check_thrid_party_requets(driver,domain_url)
    cookies = check_cookies(driver)
    if(len(cookies) > 0 or len(thrid_party_calls) > 0):
        result_dict["https://"+domain_url+"/"+url] = {"third-party-requests":thrid_party_calls,"cookies":cookies}

    #add url to list of visited urls so that it is not visited twice
    list_of_visited_urls.append(url)
    html = driver.getHtml()

    #get all urls in href and src elements
    pattern = '((?:href|src)=")([^"]+)(")'
    all_links_on_webpage = re.findall(pattern,html)

    #filter links to only include urls from own domain and remove links to resources (css, js)
    #either the link starts with / or with the domain
    own_domain_links = []
    for link in all_links_on_webpage:
        src_url = link[1]
        if(re.match("^http(s)?://"+"(.+\.)?"+domain_url,src_url) or not re.match("^http(s)?://",src_url)):
            #remove domain and protocol from url
            src_url = re.sub("http(?:s)?:\/\/(?:[\w-]+\.)*([\w-]{1,63})(?:\.(?:\w{3}|\w{2}))(?:$|\/)","",src_url)

            if(src_url.find(".") != -1 or src_url.find(":") != -1):
                continue
            #remove whitespace
            src_url = src_url.strip()
            if(src_url==""):
                continue
            #remove beginning and tailing /
            if(src_url[0] == "/"):
                src_url = src_url[1:]
            if(src_url==""):
                continue
            if(src_url[-1] == "/"):
                src_url = src_url[0:-1]
            if(src_url==""):
                continue
            
            #remove url params
            src_url = src_url.split("?")[0]

            #remove #
            src_url = src_url.split("#")[0]
            
            #it is a valid url!
            own_domain_links.append(src_url)
    
    for own_domain_link in own_domain_links:
        crawl_links(result_dict,driver,domain_url,list_of_visited_urls,number_of_visited_pages,own_domain_link)

    return

def analyse_url(url):

    def analyse_url_inner(number_of_visited_pages):

        #create variables for data collection
        list_of_visited_urls = []
        result_dict = {}

        #init the driver
        driver = SeleniumConnector()
        #driver = GhostPyConnector()

        #crawl url and sub-urls and analyse them
        crawl_links(result_dict,driver,url,list_of_visited_urls,number_of_visited_pages,'')

        #close the driver
        driver.close()

        return list_of_visited_urls,result_dict

    return lambda number_of_visited_pages: analyse_url_inner(number_of_visited_pages)