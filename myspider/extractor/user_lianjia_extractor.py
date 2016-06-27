
from scrapy import log
from scrapy.http.response.html import HtmlResponse
import re

class User_lianjiaExtractor:    
    def parse(self,nodes):
        urls = []
        
        totalPage = 0
        for node in nodes:
            html = ""
            if isinstance(node, HtmlResponse):
                html = node.body
            else:
                html = node.extract()
                
            m = re.search('"totalPage":(\d+)',html)
            if m == None:
                continue
            totalPage = int(m.groups()[0])
            break
        
        for page in range(0,totalPage):
            urls.append("./pg%d/" %(page))
        return urls
