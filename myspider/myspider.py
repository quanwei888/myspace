import sys
import json
import os
import sys
sys.path.append(os.path.dirname(__file__))

import scrapy
from scrapy.http import Request
import xmltodict

from rule import Rule
from parser import Parser 
from helper import Helper


class ConfMgr:
    conf = None
    def __init__(self,confPath):
        content = open(confPath).read()
        self.conf = json.loads(content)
    
    def getName(self):
        return conf['name']
    
    def getStartUrls(self):
        startUrls = self.conf['startUrls']
        return startUrls
    
    def getRules(self):
        rulesConf = self.conf['rules']
        rules = []
        for ruleConf in rulesConf:
            rules.append(Rule(ruleConf))
        return rules

    def getParsers(self):
        parsersConf = self.conf['parsers']
        parsers = []
        for parserConf in parsersConf:
            parsers.append(Parser(parserConf))
        return parsers
             
class MySpider(scrapy.Spider):
    name = "my"        
    parsers = None
    rules = None
 
    def __init__(self):
        confPath = os.path.dirname(__file__) + "/conf.json"
        confMgr = ConfMgr(confPath)
        self.rules = confMgr.getRules()
        self.parsers = confMgr.getParsers()
        self.start_urls = confMgr.getStartUrls()
    
    def createRequet(self,url):
        return Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1'})
    
    def start_requests(self):
        for url  in self.start_urls:
            yield self.createRequet(url)
        
    def parse(self,response):
        url = response.request.url
        
        #parse
        parsers = Helper.getParsersByUrl(self.parsers, url)
        for parser in parsers:
            items = parser.parse(response)
            for item in items:
                yield item
            
        #extract link
        rules = Helper.getRulesByUrl(self.rules, url)
        for rule in rules:
            urls = rule.parse(response)
            for url in urls:
                yield self.createRequet(url)
        
 
      
