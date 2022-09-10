from src.connector import Connector

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options

class SeleniumConnector(Connector):

    def __init__(self):
        chrome_options = Options()
        #start chrome in headless mode
        chrome_options.add_argument("--headless")

        #throw all downloads away
        chrome_options.add_experimental_option("prefs",{"download.default_directory": "/dev/null"})

        # Create a new instance of the Chrome driver
        self.driver = webdriver.Chrome('./chromedriver',options=chrome_options)

    def open(self,url):
        self.driver.get(url)

    def getCookies(self):
        return self.driver.get_cookies()

    def getHtml(self):
        return self.driver.page_source

    def getThirdPartyRequets(self):
        requets = self.driver.requests
        return list(map(lambda request:request.url,requets))

    def clearRequets(self):
        del self.driver.requests

        
    def close(self):
        #close the driver
        self.driver.quit()