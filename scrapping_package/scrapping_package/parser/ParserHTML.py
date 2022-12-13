import json
import validators
class ParserHTML:
    number_parsers=0 #number of all parsers
    def __init__(self,dict_responses,name_parser):
        """
        :param dict_responses: dict type ({URL0:content,URL1:content1,...})
        :param name_parser: name_id of ParserHTML where is the id of the parser (str)
        """
        self.dict_responses=dict_responses
        self.name_parser=name_parser + f"_id{self.number_parsers}.json"
        self.verify_types()
        self.number_parsers+=1

    def verify_types(self):
        """
        Verify the types of attributes of instance
        """
        if not type(self.dict_responses) is dict:
            raise TypeError(f"{self.dict_responses.__repr__} should be a dict.")
        for url in self.dict_responses.keys():
            if not validators.url(url) :#verify if it's url
                raise TypeError(f"{url} key from {self.dict_responses.__repr__} should be a url.")
        if not isinstance(self.name_parser,str):
            raise TypeError(f"{self.name_parser} should be a str.")

    def parse_all(self):
        """
        handle all responses and return a dictonnary ({"URL 0":element_selected_in_URL0,"URL 1":element_selected_in_URL1...}
        """
        dict_responses_all={}
        for url,content_url in zip(self.dict_responses.keys(),self.dict_responses.values()):
            dict_feats_content=self.parse(content_url)
            if not type(dict_feats_content) is dict:
                raise TypeError(f"Error in parse (wrong type return), {dict_feats_content.__repr__} should be a dict.")
            dict_responses_all[url]=dict_feats_content
        return dict_responses_all

    def parse(self,response):
        """
        :param response: binary content of request
        :return: dictionary of features selected from response
        """
        raise NotImplementedError("Parser HTML {self.name_parser} should be implemented.")

    def write(self,file_name=None,mode="w"):
        """
        :param file_name: name of the file
        :param mode: the mode of writting (default "w")
        Write the dictionnary return by parse_all into file file_name.
        """
        if file_name == None:
            file_name=self.name_parser
        else:
            if not isinstance(file_name,str):
                raise TypeError(f"{file_name} should be a str.")
            if mode != 'w' and  mode != 'wb' and  mode != 'a' and  mode != 'ab':
                raise TypeError(f"{mode} should be in {'w','wb','a','ab'}.")
        dict_responses_all=self.parse_all()
        with open(file_name,mode) as f:
            f.write(json.dumps(dict_responses_all,ensure_ascii=False)) #ensure_ascii=False to have non ascii character to unicode character



