# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def process_price(value):
    value = value.replace(' ', '')
    try:
        return int(value)
    except:
        return value


class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    pictures = scrapy.Field()
