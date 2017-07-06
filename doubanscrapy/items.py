# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MovieItem(scrapy.Item):

    # 名称
    name = scrapy.Field()

    # 年份
    year = scrapy.Field()

    # 区域(list)
    region = scrapy.Field()

    # 评级
    stars = scrapy.Field()

    # 上映日期(list列表)
    runtime = scrapy.Field()

    # 类型（list列表）
    types = scrapy.Field()

    # 导演（list列表）
    directors = scrapy.Field()

    # 主演（list列表）
    actors = scrapy.Field()

    # 语言
    language = scrapy.Field()

    # 时长（分钟）
    duration = scrapy.Field()

    # 详情链接
    detailurl = scrapy.Field()

    # IMDB链接
    IMDburl = scrapy.Field()
