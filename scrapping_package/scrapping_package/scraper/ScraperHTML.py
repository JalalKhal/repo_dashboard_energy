from Scraper import *
import lxml.html
from lxml.html.clean import Cleaner

class ScaperHTML:
    def __init__(self,start_urls):
        """
        :param start_urls:list of urls (list)
        """
        self.start_urls=start_urls
        self.verify_types()

    def verify_types(self):
        assert isinstance(self.start_urls,list)
        for url in self.start_urls:
            assert isinstance(url,str) #test if it's str
            assert validators.url(url) #test if it's url


    def start_requests(self):
        scraper=Scraper(self.start_urls)




    def write(self,response):
        """
        :param response: binary content of request
        """
        raise NotImplementedError(f'parse method is not defined ! :{self}')






