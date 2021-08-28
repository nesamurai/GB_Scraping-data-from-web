import pymongo
import requests
from lxml import html


myclient = pymongo.MongoClient("mongodb://localhost:27017")
lenta_db = myclient['lenta']
news_col = lenta_db['news']

url = "https://lenta.ru/"
response = requests.get(url)
whole_page = html.fromstring(response.text)

# main_news = page.xpath("//section[contains(@class, 'b-yellow-box')]")

main_news = whole_page.xpath("//div[@class='span4']/div[@class='first-item' or @class='item']")
for article in main_news:
    article_info = {}
    title = article.xpath(".//a[contains(@href, 'news')]/text()")
    link = article.xpath(".//a[contains(@href, 'news')]/text()/../@href")
    publication_date = article.xpath(".//a[contains(@href, 'news')]/text()/../time/@title")
    article_info['title'] = title
    article_info['link'] = link
    article_info['publication_date'] = publication_date
    news_col.insert_one(article_info)
