from abc import ABC, abstractmethod

class Connector(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def open(self,url):
        pass


    @abstractmethod
    def getCookies(self):
        pass

    @abstractmethod
    def getHtml(self):
        pass

    @abstractmethod
    def getThirdPartyRequets(self):
        pass

    @abstractmethod
    def close(self):
        pass
