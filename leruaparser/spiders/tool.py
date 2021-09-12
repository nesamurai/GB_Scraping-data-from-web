import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leruaparser.items import LeruaparserItem


class ToolSpider(scrapy.Spider):
    name = 'tool'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/search/?q=%D0%B4%D1%80%D0%B5%D0%BB%D1%8C']

    def parse(self, response: HtmlResponse):
        tools_links = response.xpath('//a[@data-qa="product-name"]')
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)
        for link in tools_links:
            yield response.follow(link, callback=self.parse_tool)

    def parse_tool(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("price", '//span[@slot="price"]/text()')
        loader.add_xpath("pictures", '//img[@alt="product image"]/@src')
        yield loader.load_item()
