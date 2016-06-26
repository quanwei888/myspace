
from helper import Helper
class Parser:
    name = None
    url = None
    fields = None
    xpath = None
    
    
    def __init__(self,conf): 
        self.name = conf['name']
        self.url = conf['url']
        self.xpath = conf.get('xpath','')
        self.fields = []         
        for fieldConf in conf['fields']:
            field = Helper.createField(fieldConf['type'],fieldConf)
            self.fields.append(field)
        
    def setFields(self,fields):
        self.fields = fields

    def parse(self,response):
        results = []
        
        nodes = [response]
        if self.xpath != "":
            nodes = response.xpath(self.xpath)
            
        for node in nodes:            
            item = {'__NAME':self.name}
            for field in self.fields:
                item[field.name] = field.parse(node)
            results.append(item)
            
        return results