from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


# preparing db
client = MongoClient('localhost', 27017)
letters_db = client['letters']
inbox_collection = letters_db['inbox']

# preparing driver
chrome_options = Options()
chrome_options.add_argument('start-maximized')
link = "https://e.mail.ru/inbox/"

try:
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(6)
    browser.get(link)

    # entering login
    login_field = browser.find_element_by_css_selector("input[name=username]")
    login_field.send_keys("study.ai_172@mail.ru")
    to_pwd_button = browser.find_element_by_css_selector("[type=submit]")
    to_pwd_button.click()

    # entering password
    pwd_field = browser.find_element_by_css_selector("input[name=password]")
    pwd_field.send_keys("NextPassword172???")
    entrance = browser.find_element_by_css_selector("[type=submit]")
    entrance.click()


    # main process

    inbox_letters = []
    letter_counter = 1

    while letter_counter < 1000:

        try:
            letter = browser.find_element_by_xpath(f'//div[@class="dataset__items"]/a[{letter_counter}]')
            letter_info = {}
            sender = letter.find_element_by_class_name("ll-crpt")
            letter_info['sender'] = sender.text
            sending_date = letter.find_element_by_xpath('//div[@class="llc__item llc__item_date"]')
            letter_info['date'] = sending_date.get_attribute('title')
            theme = letter.find_element_by_class_name("ll-sj__normal")
            letter_info['theme'] = theme.text
            inbox_letters.append(letter_info)

            letter.send_keys(Keys.ARROW_DOWN)

            if letter_counter != 29:
                letter_counter += 1
            else:
                letter_counter = 17

        except StaleElementReferenceException:
            continue
        except:
            letter_counter = 1000


finally:
    browser.quit()

# eliminate duplicated
inbox_without_duplicates = []
for item in inbox_letters:
    if item not in inbox_without_duplicates:
        inbox_without_duplicates.append(item)

for item in inbox_without_duplicates:
    inbox_collection.insert_one(item)
