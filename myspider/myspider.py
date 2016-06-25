import scrapy
import xmltodict
import sys
sys.path.append(sys.path[0])

print sys.path
from rule import Rule
from parser import Parser
from field import Field

class MySpider(scrapy.Spider):
    name = "my"
    start_urls = (
        'https://www.sogou.com/web?query=qq',
        )
    
    parser = None
    fields = None
    startUrls = None
    rules = None
 
    def __init__(self):
        self.init()
    
    
    def init(self):
        self.initConf() 
   
    def parse(self,response):
        pass 

    
    def initConf(self):
        fileName = "./spider.xml"
        content = open(fileName).read() 
        conf = xmltodict.parse(content)
        conf = conf['spider']

        print conf
        self.name = conf['name']
        self.startUrls = conf['startUrls']
        self.initRules(conf)
        self.initParsers(conf)
        
    
    def initRules(self,conf):
        rulesConf = conf['rules']
        for ruleConf in rulesConf:
            rule = Rule(ruleConf['fromUrlPattern'],ruleConf['toUrlPattern'])
            self.rules.append(rule)
    
    def initParsers(self,conf):
        parsersConf = conf['parsers']
        for parserConf in parsersConf:
            parser = Parser(parserConf['urlPattern'])
            fields = []
            for fieldConf in parserConf['fields']:
                field = Field(fieldConf['name'],fieldConf['type'],
                    fieldConf['xpath'],fieldConf['cssPath'])
                fields.append(field)
            parser.setFields(fields)
            self.parsers.append(parser)

    def parse(self,response):
        url = response.request.url

        parser = self.getParserByUrl(url)
        data = parser
        
    def getParserByUrl(self,url):
        pass
