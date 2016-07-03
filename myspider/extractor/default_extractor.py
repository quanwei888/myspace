
from scrapy import log

class DefaultExtractor:    
    def parse(self,nodes):
        urls = []
        
        for node in nodes:
            urlNodes = node.xpath(".//a/@href").extract()
            for url in urlNodes:
                urls.append(url)
        return urls
