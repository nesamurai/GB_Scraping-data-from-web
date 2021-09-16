# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class LeruaparserPipeline:
    def process_item(self, item, spider):
        return item


class LeruaPicturesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img in item['pictures']:
            try:
                yield Request(img)
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        item['pictures'] = [elem[1] for elem in results if elem[0]]
        return item
