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
            if category_url.css("::attr(has_child)").extract_first() == '1':
                header = category_url.css("h3::text").extract_first()
                for sub_category_url in category_url.css("ol.nobt li[has_child]"):
                    sub_header = sub_category_url.css("a h4::text").extract_first()
                    count = sub_category_url.css("a p:nth-child(3)::text").extract_first()
                    class_id = sub_category_url.css("::attr(class_id)").extract_first()
                    url = "http://word.iciba.com/?action=courses&classid=" + str(class_id)
                    #print("<<%s>>%s=======================>%s,url:%s" %(header,sub_header,count,url))
                    yield response.follow(url, callback=self.parse_chapter_url,meta={"header":header,"sub_header":sub_header,\
                        "count":count})
            else :
                header = category_url.css("h3::text").extract_first()
                sub_header = ""
                count = category_url.css('p::text').extract_first()
                class_id = category_url.css("::attr(class_id)").extract_first()
                url = "http://word.iciba.com/?action=courses&classid=" + str(class_id)
                #print("%s=======================>%s,url::%s"%(header,count,url))
                yield response.follow(url, callback=self.parse_chapter_url,meta={"header":header,"sub_header":sub_header,\
                        "count":count})

    def parse_chapter_url(self,response):
        for chapter_url in response.css("ul.study-speed-m li.c_panel"):
            header = response.meta["header"]
            sub_header = response.meta["sub_header"]
            count = response.meta["count"]
            class_id = response.request.url.split('=')[-1]
            course_id = chapter_url.css("::attr(course_id)").extract_first()
            word_url = "http://word.iciba.com/?action=words&class=" + str(class_id) + "&course=" + str(course_id)
            #print(word_url)
            yield response.follow(word_url, callback=self.parse_word,meta={"header":header,"sub_header":sub_header,\
                        "count":count})

    def parse_word(self,response):
        for info in response.css("ul.word_main_list li"):
            yield{
            'header':response.meta["header"],
            'sub_header':response.meta["sub_header"],
            'count':response.meta["count"],
            'word':info.css("div.word_main_list_w span::text").extract_first().strip(),
            'phonetic':info.css("div.word_main_list_y strong::text").extract_first().strip(),
            'chinese':info.css("div.word_main_list_s span::attr(title)").extract_first().strip()
            #print(header,sub_header,count,word,phonetic,chinese)
            }