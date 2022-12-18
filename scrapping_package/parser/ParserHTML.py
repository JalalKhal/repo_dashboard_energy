import asyncio
import json
from scrapping_package.scraper.Scraper import Scraper
class ParserHTML:
    DATAPATH="./data"
    DATAPATHCACHE="./data_cache"

    def __init__(self,starts_url,session,name_parser,datapath=DATAPATH,datapath_cache=DATAPATHCACHE):
        """
        :param name_parser: name of ParserHTML
        :param session: asynchronous session aiohttp
        """
        self.name_parser=name_parser
        self.starts_url=starts_url
        self.session=session
        self.dict_responses={}
        self.datapath=datapath
        self.datapath_cache=datapath_cache
        self.verify_types()

    def verify_types(self):
        """
        Verify the types of attributes of instance
        """
        if not isinstance(self.name_parser,str):
            raise TypeError(f"{self.name_parser} should be a str.")

    async def parse_init(self):
        """
        :return: self.dict_respones=dictionnary of start_urls
        IMPORTANT parse_init NEED TO BE CALLED
        """
        scraper_init=Scraper(self.starts_url,name_scraper="url_init_parser")
        self.dict_responses=await scraper_init.agets(self.session)



    async def parse(self,responses):
        """
        :param responses: list of binary contents of requests
        :return: dictionary of all urls of features selected from url content
        """
        raise NotImplementedError("Parser HTML {self.name_parser} should be implemented.")

    def write(self,dict_all):
        """
        :param dict_all: return of parse
        """
        with open(f"{self.datapath_cache}/output_cache.json", "a") as f:
            f.write(json.dumps(dict_all,ensure_ascii=False))
        with open(f"{self.datapath}/output.json", "a") as f:
            f.write(json.dumps(dict_all,ensure_ascii=False))

    @classmethod
    def split(cls,urls, n):
        """
        split the lists of urls in parts
        """
        k, m = divmod(len(urls), n)
        return [urls[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)]





