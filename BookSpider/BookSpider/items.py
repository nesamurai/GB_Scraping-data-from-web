# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookspiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    basic_price = scrapy.Field()
    stock_price = scrapy.Field()
    rating = scrapy.Field()
    _id = scrapy.Field()
