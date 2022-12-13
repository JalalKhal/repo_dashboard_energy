from ParserHTML import ParserHTML
from scrapping_package.scraper.Scraper import Scraper
import aiohttp
import asyncio
import json

class CentraleParser(ParserHTML):

    def __init__(self,dict_responses):
        super().__init__(dict_responses,self.__class__.__name__)



    def parse(self,response):
        return {"0":response}




if __name__=="__main__":
    urls=[]
    with open("/home/khaldi/DataspellProjects/dsProject/scrapping/scraper/data_firstlev.json","r") as f:
        dict_content=json.loads(''.join(f.readlines()))
        for url,sub_urls in zip(dict_content.keys(),dict_content.values()):
            urls+=sub_urls
    scraper=Scraper(urls[:1],file_name="data_secondlev_bis.json")
    async def f():
        async with aiohttp.ClientSession() as session:
            return await scraper.agets(session)


    cen=CentraleParser(asyncio.run(f()))
    cen.write()

