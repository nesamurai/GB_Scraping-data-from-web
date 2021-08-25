import requests

from bs4 import BeautifulSoup
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['vacancies_db']
vacancies_collection = db['vacancies']


def push_new_to_db(vacancy):
    if vacancies_collection.find_one({
        "title": vacancy["title"],
        "link": vacancy["link"],
        "employer": vacancy["employer"],
        "location": vacancy["location"],
        "$or": [
                {"salary": None},
                {"min_salary": vacancy['min_salary'], "max_salary": vacancy['max_salary'],
                "currency": vacancy['currency']}
            ]
        }):
        return None
    else:
        result = vacancies_collection.insert_one(vacancy)
        return return result.inserted_id


text = input("Введите должность (например 'python developer'): ")
url = 'https://hh.ru/search/vacancy'

params = {
    "area": "1",
    "fromSearchLine": "true",
    "st": "searchVacancy",
    "text": text
}
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}

x = requests.get(url, params=params, headers=headers)
soup = BeautifulSoup(x.text, 'html.parser')

pages_list = []
for page in soup.find_all(attrs={'data-qa': 'pager-page'}):
    pages_list.append(page.span.get_text())
# print(pages_list)


for page in pages_list:
    params = {
        "area": "1",
        "fromSearchLine": "true",
        "st": "searchVacancy",
        "text": text,
        "page": page
    }
    x = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(x.text, 'html.parser')

    vacancy_divs = soup.find_all('div', {'class': 'vacancy-serp-item'})
    for vacancy_div in vacancy_divs:

        vacancy_title_extracted = vacancy_div.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        vacancy_title = vacancy_title_extracted.get_text()

        try:
            vacancy_salary_extracted = vacancy_div.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            salary = vacancy_salary_extracted.get_text()
        except:
            salary = None

        vacancy_link = vacancy_div.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).get('href')

        vacancy_employer_extracted = vacancy_div.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
        vacancy_employer = vacancy_employer_extracted.get_text().replace("\xa0", " ")

        vacancy_location_extracted = vacancy_div.find('span', {'data-qa': 'vacancy-serp__vacancy-address'})
        vacancy_location = vacancy_location_extracted.get_text()


        vacancy_informaion = {}
        vacancy_informaion['title'] = vacancy_title
        vacancy_informaion['link'] = vacancy_link
        vacancy_informaion['employer'] = vacancy_employer
        vacancy_informaion['location'] = vacancy_location

        if salary is not None:
            dash = chr(8211)
            p = chr(1088)
            if dash in salary and p in salary:
                idx_dash = salary.find(dash)
                idx_p = salary.find(p)
                idx_point = salary.find('.')
                min_salary = salary[:idx_dash - 1].replace("\u202f", "")
                min_salary = int(min_salary)
                max_salary = salary[idx_dash + 2:idx_p - 1].replace("\u202f", "")
                max_salary = int(max_salary)
                currency = salary[idx_p:idx_point]
            elif 'от' in salary and p in salary:
                idx_p = salary.find(p)
                idx_point = salary.find('.')
                min_salary = salary[3:idx_p - 1].replace("\u202f", "")
                min_salary = int(min_salary)
                max_salary = None
                currency = salary[idx_p:idx_point]
            elif 'до' in salary and p in salary:
                idx_p = salary.find(p)
                idx_point = salary.find('.')
                min_salary = None
                max_salary = salary[3:idx_p - 1].replace("\u202f", "")
                max_salary = int(max_salary)
                currency = salary[idx_p:idx_point]
            elif 'от' in salary and 'USD' in salary:
                idx_u = salary.find('U')
                min_salary = salary[3:idx_u - 1].replace("\u202f", "")
                min_salary = int(min_salary)
                max_salary = None
                currency = salary[idx_u:]
            elif 'до' in salary and 'USD' in salary:
                idx_u = salary.find('U')
                min_salary = None
                max_salary = salary[3:idx_u - 1].replace("\u202f", "")
                max_salary = int(max_salary)
                currency = salary[idx_u:]
            elif dash in salary and 'USD' in salary:
                idx_dash = salary.find(dash)
                idx_u = salary.find('U')
                min_salary = salary[:idx_dash - 1].replace("\u202f", "")
                min_salary = int(min_salary)
                max_salary = salary[idx_dash + 2:idx_u - 1].replace("\u202f", "")
                max_salary = int(max_salary)
                currency = salary[idx_u:]
            else:
                min_salary = None
                max_salary = None
                currency = None
            vacancy_informaion['min_salary'] = min_salary
            vacancy_informaion['max_salary'] = max_salary
            vacancy_informaion['currency'] = currency
        else:
            vacancy_informaion['salary'] = salary

        push_new_to_db(vacancy_informaion)
