# _*_ coding:utf-8 _*_

'''
Author:sea85
Date:2019/7/30
抓取爱词吧所有分类单词
'''

import scrapy

class IcibaSpider(scrapy.Spider):

    name = 'Iciba'
    start_urls = ["http://word.iciba.com/"]

    def parse(self,response):
        for category_url in response.css("div.main_l #mainwordlist > li[has_child]"):
            has_child = category_url.css("::attr(has_child)").extract_first()
            header = category_url.css("h3::text").extract_first()
            count = category_url.css('p::text').extract_first()
            print("%s=======================>%s"%(header,count),has_child)
