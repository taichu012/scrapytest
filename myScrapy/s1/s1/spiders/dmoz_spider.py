# -*- coding: utf-8 -*-
"""
Created on Sun Apr 03 10:41:17 2016
dmoz spider

@author: User
"""

from cctool import ct

from scrapy.spiders import Spider

from ..items import DmozItem


# from scrapy.selector import Selector
#
# def list2str(str):
#    '''
#    这个函数将传入的�?维列表合并成字符串，并去掉两边空格后添加[]并返回�??
#    '''
#    return  "["+"".join(itertools.chain(*str)).strip()+"]"
#
class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
]    
  
    
    def parse4Print(self, response):
        # hxs = HtmlXPathSelector(response)
        # sites = hxs.xpath('//fieldset/ul/li')
        sites = response.xpath('//fieldset/ul/li')
        # sites = hxs.path('//ul/li')
        for site in sites:
            title = site.xpath('a/text()').extract()
            link = site.xpath('a/@href').extract()
            # desc = site.xpath('text()').extract()
            desc = site.xpath('text()').re(r'(\w| )+?')
            desc = ct.list2str(desc)
            # print title, link, desc
            print title, link, desc
            
            
    def parse(self, response):
        # hxs = HtmlXPathSelector(response)
        # sites = hxs.xpath('//fieldset/ul/li')
        sites = response.xpath('//fieldset/ul/li')
        # sites = hxs.path('//ul/li')
        items = []
        for site in sites:
            item = DmozItem()
            item['title'] = site.xpath('a/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            desc = site.xpath('text()').re(r'(\w| )+?')
            # print desc
            item['desc'] = ct.list2str(desc)
            items.append(item)
        return items
        
        

        
        
