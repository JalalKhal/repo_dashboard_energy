import validators
class ScraperEcom:
    headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
             "Accept-Language":"fr;q=0.9",
             "Accept-Encoding":"gzip, deflate",
             "Accept":"text/html",
             "referer":"'https://www.google.com/'",
    } #headers of requests
    file_name="output.json"

    def __init__(self,urls,headers=headers,file_name=file_name,name_scraper='ScraperDefault'):
        """
        :param name_scraper: name of instance of class ScraperEcom (str)
        :param urls: list of urls (list of url)
        :param headers: headers request (dictionnary)
        :param file_name: file name of file contains requests content (str)
        """
        self.name_scraper=name_scraper
        self.urls=urls
        self.headers=headers
        self.file_name=file_name
        ScraperEcom.verify_types(self)

    def verify_types(self):
        """
        Verify the types of attributes of instance
        """
        for url in self.urls:
            if not isinstance(url,str):
                raise TypeError(f"{url}  from {self.urls} should be a str.")
            if not validators.url(url) :#verify if it's url
                raise TypeError(f"{url} from {self.urls} should be a url.")
        if not isinstance(self.name_scraper,str):
            raise TypeError(f"{self.name_scraper} should be a str.")
        if not isinstance(self.file_name,str):
            raise TypeError(f"{self.file_name} should be a str.")
        if not type(self.headers) is dict:
            raise TypeError(f"{self.headers}  should be a dict.")

    def __repr__(self):
        return f"ScraperECOM: {self.name_scraper}"

    def get(self,*args,**kwargs):
        """
        :param args:non keywords parameters
        :param kwargs: keywords parameters
        :return: return contents of urls
        """
        pass

    def write(self,*args,**kwargs):
        """
        :param args:non keywords parameters
        :param kwargs: keywords parameters
        write content of urls into file self.file_name
        """
        pass



if __name__=="__main__":
    s=ScraperEcom(["http://www.goo.fr"],headers={0:0},file_name="slsl",name_scraper="ScraperAmazon")
    s.write(5,4,2,lib="lzlz")
    print(s.__repr__())



