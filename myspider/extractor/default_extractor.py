

class DefaultExtractor:    
    def parse(self,response):
        urls = []        
        return response.xpath("//a/@href").extract()
