import scrapy

class Spider(CrawlSpaider):
    name = "spider"
    parser = None
    fields = None
    name = None
    startUrls = None
    rules = None
    

    def start_requests(self):
        return [make_requests_from_url("https://www.baidu.com/s?wd=qq")]

    
    def initConf(self):
       content = open(file).read() 
       conf = xmltodict.parse(content)
       conf = conf['spider']

       self.name = conf['name']
       self.startUrls = conf['startUrls']
       self.initRules(conf)
       self.initParsers(conf)
        
    
    def initRules(self,conf):
        rulesConf = conf['rules']
        for ruleConf in rules:
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

