from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re


chrome_options = Options()
#start chrome in headless mode
chrome_options.add_argument("--headless")

#throw all downloads away
chrome_options.add_experimental_option("prefs",{"download.default_directory": "/dev/null"})

# Create a new instance of the Chrome driver
driver = webdriver.Chrome('./chromedriver',options=chrome_options)

def check_thrid_party_requets(driver,domain_url):
    thrid_party_calls = []
    for request in driver.requests:
        if request.response:
            #check if url is from a thrid party
            request_url = request.url
            if(not re.match("^http(s)?://"+"(www\.)?"+domain_url,request_url)):
                #remove slash and just use adress
                request_url = request_url.replace("https://","")
                request_url = request_url.replace("http://","")
                request_url = request_url.split("/")[0]
                thrid_party_calls.append(request_url)
    del driver.requests
    #remove list without doubles
    return list(dict.fromkeys(thrid_party_calls))

def check_cookies(driver):
    cookies = driver.get_cookies()
    return cookies

def crawl_links(result_dict,driver,domain_url,list_of_visited_urls,url):

    #check if url was already visited
    if(url in list_of_visited_urls):
        return

    #get page content
    print("Visiting: "+"https://www."+domain_url+"/"+url)
    driver.get("https://www."+domain_url+"/"+url)


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
        result_dict["https://www."+domain_url+"/"+url] = {"third-party-requests":thrid_party_calls,"cookies":cookies}

    #add url to list of visited urls so that it is not visited twice
    list_of_visited_urls.append(url)
    html = driver.page_source

    #get all urls in href and src elements
    pattern = '((?:href|src)=")([^"]+)(")'
    all_links_on_webpage = re.findall(pattern,html)

    #filter links to only include urls from own domain and remove links to resources (css, js)
    #either the link starts with / or with the domain
    own_domain_links = []
    for link in all_links_on_webpage:
        src_url = link[1]
        if(re.match("^http(s)?://"+"(www\.)?"+domain_url,src_url) or not re.match("^http(s)?://",src_url)):
            #remove domain and protocol from url
            src_url = src_url.replace("https://","")
            src_url = src_url.replace("http://","")
            src_url = src_url.replace("www.","")
            src_url = src_url.replace(domain_url,"")
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
        crawl_links(result_dict,driver,domain_url,list_of_visited_urls,own_domain_link)

    return


list_of_visited_urls = []
result_dict = {}
crawl_links(result_dict,driver,"sapotec.at",list_of_visited_urls,'')
print(list_of_visited_urls)
print(len(list_of_visited_urls))
print(result_dict)
driver.quit()