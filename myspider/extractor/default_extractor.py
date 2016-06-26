
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

class DefaultExtractor:    
    def parse(self,response):
        urls = []        
        nodes = response.xpath("//a/@href").extract()
        baseUrl = get_base_url(response)
        for node in nodes:
            urls.append(urljoin_rfc(baseUrl, node))
        return urls
