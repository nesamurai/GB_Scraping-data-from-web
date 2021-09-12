import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['mvideo']
mycol = mydb['hits']

chrome_options = Options()
chrome_options.add_argument('start-maximized')

link = "https://www.mvideo.ru/"
browser = webdriver.Chrome(options=chrome_options)
browser.get(link)

hits_list = browser.find_element_by_xpath('//div[@class="main-container"]/div[@class="facelift gallery-layout products--shelve gallery-layout_products gallery-layout_product-set grid-view"][1]')


arrow_btn = hits_list.find_element_by_xpath('.//a[contains(@class, "arrow-right")]')

final_array = []

products = hits_list.find_elements_by_tag_name("li")
for product in products:
    info = {}
    title = product.find_element_by_tag_name("h3")
    info['title'] = title.text
    price = product.find_element_by_class_name("fl-product-tile-price__current")
    info['price'] = price.text
    final_array.append(info)


a = 1
while a > 0:
    try:
        btn_disabled = hits_list.find_element_by_xpath('.//a[contains(@class, "arrow-right disabled")]')
        a = -1

    except:
        arrow_btn.click()
        time.sleep(1)
        products = hits_list.find_elements_by_tag_name("li")
        for product in products:
            info = {}
            title = product.find_element_by_tag_name("h3")
            info['title'] = title.text
            price = product.find_element_by_class_name("fl-product-tile-price__current")
            info['price'] = price.text
            if info not in final_array:
                final_array.append(info)


for item in final_array:
    if item['title'] == '' or item['price'] == '':
        final_array.remove(item)
    else:
        mycol.insert_one(item)

browser.quit()
