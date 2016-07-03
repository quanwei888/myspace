
from helper import Helper
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy import log

class Rule:
    fromUrl = None
    toUrl = None
    extractor = None
    xpath = None

    def __init__(self,conf):
        self.fromUrl = conf['from']
        self.toUrl = conf['to']
        self.xpath = conf['xpath']
        self.extractor = Helper.createExtractor(conf['extractor']) 
    
    def parse(self,response):        
        urls= []
        
        nodes = [response]
        if self.xpath != "":
            nodes = response.xpath(self.xpath)
        
        if len(nodes) == 0:
            return urls
        
        baseUrl = get_base_url(response)
        for url in self.extractor.parse(nodes):
            url = urljoin_rfc(baseUrl, url)
            #log.msg(url, level=log.WARNING)
            if Helper.canMatch(self.toUrl,url):
                urls.append(url)
                log.msg("Link:" + url)
                #break
        
        return urls