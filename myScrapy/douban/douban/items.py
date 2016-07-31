# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# import scrapy #default import 是低效率的，导入太多子模块了�?
from scrapy import Item, Field  # 只导入需要的子模块！


# item definition
class DoubanItem(Item):
    movie_name = Field()
    movie_director = Field()
    movie_writer = Field()
    movie_roles = Field()
    movie_language = Field()
    movie_date = Field()
    movie_long = Field()
    movie_description = Field()
    
    
