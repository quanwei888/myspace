
import urllib
import urllib2
import json

class WordHelper(): 
    url = "http://nj02.nlpc.baidu.com/%s?username=quanwei01&app=nlpc_201604081411031&encoding=utf8"
   
    def __init__(self):
        pass
    
    @classmethod
    def loadHttp(self, toolName, postData):
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        #postData = urllib.urlencode(postData)
        #postData = json.dumps(postData)
        reqUrl = self.url % (toolName)
        req = urllib2.Request(url=reqUrl, data=postData)
        urllib2.socket.setdefaulttimeout(10)
        res = urllib2.urlopen(req)
        resData = res.read()
        print resData
        return json.loads(resData)
    
    @classmethod
    def wordseg(self, query):
        param = '{"lang_id":1,"lang_para":0,"query":"%s"}' % (query)
        return self.loadHttp("nlpc_wordseg_3016", param)
    @classmethod
    def wordrank(self, query):
        param = '{"lang_id":1,"lang_para":0,"query":"%s"}' % (query)
        return self.loadHttp("nlpc_wordrank_208", param)
    @classmethod
    def wordner(self, query):
        param = '{"lang_id":1,"lang_para":0,"query":"%s"}' % (query)
        return self.loadHttp("nlpc_wordner_300", param)
    @classmethod
    def wordpos(self, query):
        param = '{"lang_id":1,"lang_para":0,"query":"%s"}' % (query)
        return self.loadHttp("nlpc_wordpos_202", param)
    @classmethod
    def textsim(self, query1,query2):
        param = '{"query1":"%s","query2":"%s"}' % (query1,query2)
        return self.loadHttp("nlpc_textsim_103", param)
