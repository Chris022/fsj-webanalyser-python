from src.connector import Connector

from ghost import Ghost

class GhostPyConnector(Connector):

    def __init__(self):
        ghost = Ghost()
        self.session = ghost.start()

    def open(self,url):
        self.page, self.extra_resources = self.session.open(url)

    def getCookies(self):
        return self.session.cookies

    def getHtml(self):
        return str(self.page.content)

    def getThirdPartyRequets(self):
        return list(map(lambda resource: resource.url,self.extra_resources))

    def clearRequets(self):
        pass
        
    def close(self):
        pass