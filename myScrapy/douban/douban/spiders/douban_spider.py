# -*- coding: utf-8 -*-
"""
Created on Sun Apr 03 10:41:17 2016
douban spider

@author: User
"""

from cctool import ct
import re
import sys

from scrapy.http import Request
from scrapy.spiders import Spider

from myScrapy.douban.douban.items import DoubanItem


# Python2.5+ 初始化后会删�? sys.setdefaultencoding 这个方法，我们需要重新载�? 
reload(sys)
# python默认环境编码是ascii
sys.setdefaultencoding("utf-8")
# from scrapy.selector import Selector
# sys.path.append('myScrapy.douban.douban')
    

class DoubanSpider(Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = []    
  
    def start_requests(self):
        file_object = open('movie_name.txt', 'r')

        try:
            url_head = "http://movie.douban.com/subject_search?search_text="
            for line in file_object:
                self.start_urls.append(url_head + line)
            
            for url in self.start_urls:
                yield self.make_requests_from_url(url)
        finally:
            file_object.close()
            # years_object.close()

    def parse(self, response):
        # open("test.html",'wb').write(response.body)
        # hxs = HtmlXPathSelector(response)
        # movie_link = hxs.select('//*[@id="content"]/div/div[1]/div[2]/table[1]/tr/td[1]/a/@href').extract()
        movie_link = response.xpath('//*[@id="content"]/div/div[1]/div[2]/table[1]/tr/td[1]/a/@href').extract()

        if movie_link:
            yield Request(movie_link[0], callback=self.parse_item)
        
        
    def parse_item(self, response):
        # hxs = HtmlXPathSelector(response)
        # movie_name = hxs.select('//*[@id="content"]/h1/span[1]/text()').extract()
        # movie_director = hxs.select('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        # movie_writer = hxs.select('//*[@id="info"]/span[2]/span[2]/a/text()').extract()
        movie_name = response.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        movie_director = response.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        movie_writer = response.xpath('//*[@id="info"]/span[2]/span[2]/a/text()').extract()
        
        # 爬取电影详情�?要在已有对象中继续爬�?
        # movie_description_paths = hxs.select('//*[@id="link-report"]')
        movie_description_paths = response.xpath('//*[@id="link-report"]')
        
        
        movie_description = []
        for movie_description_path in movie_description_paths:
            movie_description = movie_description_path.xpath('.//*[@property="v:summary"]/text()').extract()

        # 提取演员�?要从已有的xPath对象中继续爬我要的内�?
        movie_roles_paths = response.xpath('//*[@id="info"]/span[3]/span[2]')
        movie_roles = []
        for movie_roles_path in movie_roles_paths:
            movie_roles = movie_roles_path.xpath('.//*[@rel="v:starring"]/text()').extract()

        # 获取电影详细信息序列
        movie_detail = response.xpath('//*[@id="info"]').extract()

        item = DoubanItem()
        item['movie_name'] = ''.join(movie_name).strip().replace(',', ';').replace('\'', '\\\'').replace('\"', '\\\"').replace(':', ';')
        # item['movie_link'] = movie_link[0]
        item['movie_director'] = movie_director[0].strip().replace(',', ';').replace('\'', '\\\'').replace('\"', '\\\"').replace(':', ';') if len(movie_director) > 0 else ''
        # 由于逗号是拿来分割电影所有信息的，所以需要处理�?�号;引号也要处理，否则插入数据库会有问题
        item['movie_description'] = movie_description[0].strip().replace(',', ';').replace('\'', '\\\'').replace('\"', '\\\"').replace(':', ';') if len(movie_description) > 0 else ''
        item['movie_writer'] = ';'.join(movie_writer).strip().replace(',', ';').replace('\'', '\\\'').replace('\"', '\\\"').replace(':', ';')
        item['movie_roles'] = ';'.join(movie_roles).strip().replace(',', ';').replace('\'', '\\\'').replace('\"', '\\\"').replace(':', ';')
        # item['movie_language'] = movie_language[0].strip() if len(movie_language) > 0 else ''
        # item['movie_date'] = ''.join(movie_date).strip()
        # item['movie_long'] = ''.join(movie_long).strip()
        
        # 电影详情信息字符�?
        movie_detail_str = ''.join(movie_detail).strip()
        # print movie_detail_str

        movie_language_str = ".*语言:</span> (.+?)<br><span.*".decode("utf8")
        movie_date_str = ".*上映日期:</span> <span property=\"v:initialReleaseDate\" content=\"(\S+?)\">(\S+?)</span>.*".decode("utf8")
        movie_long_str = ".*片长:</span> <span property=\"v:runtime\" content=\"(\d+).*".decode("utf8")
        
        # 因字符串中可能包含换行符\n，如不使用re.S参数，则只在每一行内进行匹配，一行没有则换下�?行重新开始匹配�??
        # 当使用re.S参数后，正则表达式会将这个字符串作为�?个整体，在整体中进行匹配�?
        
        pattern_language = re.compile(movie_language_str, re.S)
        pattern_date = re.compile(movie_date_str, re.S)
        pattern_long = re.compile(movie_long_str, re.S)
        
        
        movie_language = re.search(pattern_language, movie_detail_str)
        movie_date = re.search(pattern_date, movie_detail_str)
        movie_long = re.search(pattern_long, movie_detail_str)

        item['movie_language'] = ""
        if movie_language:
            item['movie_language'] = movie_language.group(1).strip().replace(',', ';').replace('\'', '\\\'').replace('\"', '\\\"').replace(':', ';')
        # item['movie_detail'] = ''.join(movie_detail).strip()

        item['movie_date'] = ""
        if movie_date:
            item['movie_date'] = movie_date.group(1).strip().replace(',', ';').replace('\'', '\\\'').replace('\"', '\\\"').replace(':', ';')

        item['movie_long'] = ""
        if movie_long:
            item['movie_long'] = movie_long.group(1)

        yield item        
        

        
        
