import asyncio
import aiohttp
import json
import validators  #validator of url
import numpy.random as random
from scrapping_package.scraper import useragents #user agents file

class Scraper:

    headers={"User-Agent":"",
             "Accept-Language":"en;q=0.9",
             "Accept-Encoding":"gzip, deflate",
             "Accept":"text/html",
             "referer":"https://www.google.com",
             } #headers of requests
    requests_per_unit=1 #numbers of asynchronous requests per unit time (cf time_wait)
    time_wait=5 #time to do a pause for requesting.
    file_name="output.json" #file name of requests content
    USERAGENTS=useragents.get_user_agents() #user agents lists for popular browser
    def __init__(self,urls,name_scraper,headers=headers,requests_per_unit=requests_per_unit,\
                 time_wait=time_wait,file_name=file_name):
        """
        :param urls: list of urls (list)
        :param headers: headers request (dictionnary)
        :param requests_per_unit: numbers of asynchronous requests per unit time (int>=0)
        :param time_wait: time (second) to wait for do a new requests_per_unit (float or int >=0)
        :param file_name: file name of file contains requests content (str)
        :param name_scraper: name of Scraper.
        """
        self.urls=urls
        self.headers=headers
        self.requests_per_unit=requests_per_unit
        self.time_wait=time_wait
        self.file_name=file_name
        self.name_scraper=name_scraper
        Scraper.verify_types(self)

    def verify_types(self):
        if not isinstance(self.urls,list):
            raise TypeError(f"{self.urls} should be a list.")
        for url in self.urls:
            if not isinstance(url,str) :#test if it's str
                raise TypeError(f"{url} from {self.urls} should be a str")
            if not validators.url(url) :#test if it's url
                raise TypeError(f"{url} from {self.urls} should be a url")
        if not type(self.headers) is dict:
            raise TypeError(f"{self.headers.__repr__} should be a dict.")
        if not isinstance(self.requests_per_unit,int) and self.requests_per_unit>=0:
            raise ValueError(f"{self.requests_per_unit} should be a positive integer.")
        if not (isinstance(self.time_wait,float) or isinstance(self.time_wait,int)) and self.time_wait>=0:
            raise ValueError(f"{self.time_wait} should be a positive float or integer.")
        if not isinstance(self.file_name,str):
            raise TypeError(f"{self.file_name} should be a str.")
        if not isinstance(self.name_scraper,str):
            raise TypeError(f"{self.name_scraper} should be a str.")


    async def afetch(self,url,session):
        """
        :param url: url of website
        :param session: asynchronous session
        :return: fetch content of url from session
        """
        self.headers["User-Agent"]=random.choice(Scraper.USERAGENTS)
        async with session.get(url,headers=self.headers,proxy="http://5.39.105.211:3128") as response:
            return await response.read() #.read() return binary content

    async def agets(self,session): #coroutine
        """
            :param session: current session asynchronous of http resquests
            do asynchronous requests and set up into dictionnary ({"URL 0":content 0,"URL 1":content 1, ...})
        """
        tasks=[] #list of coroutines of all requests
        for i in range(len(self.urls)):
            task=asyncio.create_task(self.afetch(self.urls[i],session)) #create task for urls[i]
            tasks.append(task)
            if self.time_wait > 0 and (i+1)% self.requests_per_unit ==0:
                await asyncio.sleep(self.time_wait)
        responses=await asyncio.gather(*tasks,return_exceptions=True) #gather: Return Future object :need to be awaited to get result (awaitable object)
                                                                        #gather: can take as parameter task or native co-routine.

        dict_responses={self.urls[i]:response for i,response in enumerate(responses)} #.result() method from Future class
        return dict_responses


    async def awrite(self,session,mode="w"):
        """
        :param session: current session asynchronous of http resquests
        :param mode: writting mode: binary mode (wb) or writting mode (w)
        write results of requests into json file ({"URL 0":content 0,"URL 1":content 1 ...})
        """
        assert mode == "w" or mode == "wb" or mode == "a" or mode =="ab"
        dict_responses=await self.agets(session)
        urls=dict_responses.keys()
        contentsb=dict_responses.values()
        for url, contentb in zip(urls,contentsb):
            try:
                dict_responses[url]=contentb.decode("UTF-8") #get the result of co-routine.
            except UnicodeDecodeError as e:
                print(f"Erreur de décodage (UTF-8) pour l'url:{url}")
        with open(self.file_name,mode) as f:
            f.write(json.dumps(dict_responses,ensure_ascii=False)) #ensure_ascii=False to have non ascii character to unicode character

