# -*- coding: utf-8 -*-
import scrapy

import json

class FollowerSpider(scrapy.Spider):
    name = "follower"
    allowed_domains = ["weibo.cn"]
    start_urls = (
        'http://m.weibo.cn/page/json?containerid=1005051861449115_-_FOLLOWERS&page=1',
    )
    urlPattern = "http://m.weibo.cn/page/json?containerid=100505%d_-_FOLLOWERS&page=%d"

    download_delay = 0.5
    def parse(self, response):
        data = response.body
        data = json.loads(data)
        
        count = data['count']
        maxPage = 1
        if "maxPage" in data['cards'][0]:
            maxPage = (int)(data['cards'][0]['maxPage'])

        for i in range(1,maxPage + 1):
            break
            print maxPage
        
        for user in data['cards'][0]['card_group']:
            user = user['user']
            print user['id'],user['screen_name']
        yield response.request 
    def generateData(data):
        pass
         
