
from helper import Helper

class Rule:
    fromUrl = None
    toUrl = None
    extractor = None

    def __init__(self,conf):
        self.fromUrl = conf['fromUrl']
        self.toUrl = conf['toUrl']
        self.extractor = Helper.createExtractor(conf['extractor']) 
    
    def parse(self,response):
        '''
        if not Helper.canMatch(self.fromUrl,response.request.url):
            return []        
        '''
        
        urls= []
        for url in self.extractor.parse(response):
            if Helper.canMatch(self.toUrl,url):
                urls.append(url)
                break
        
        return urls