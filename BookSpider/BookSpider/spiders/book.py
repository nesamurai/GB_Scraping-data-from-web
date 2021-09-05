import scrapy
from scrapy.http import HtmlResponse
#from jobparser.items import JobparserItem
from BookSpider.items import BookspiderItem


class BookSpider(scrapy.Spider):

    name = 'fairy'
    allowed_domains = ['www.labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D1%81%D0%BA%D0%B0%D0%B7%D0%BA%D0%B8/?stype=0']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@class="product-title-link"]/@href').getall()
        next_page = response.xpath('//div[@class="pagination-next"]/a[@class="pagination-next__text"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in links:
            yield response.follow(link, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        url = response.url
        title = response.xpath('//h1/text()').get()
        authors = response.xpath('//div[@class="authors"]/a[@class="analytics-click-js"]/text()').getall()
        basic_price = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
        stock_price = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        rating = response.xpath('//div[@id="rate"]/text()').get()
        yield BookspiderItem(url=url, title=title, authors=authors, basic_price=basic_price,
        stock_price=stock_price, rating=rating)
