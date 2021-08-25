from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['vacancies_db']
vacancies_collection = db['vacancies']


def search_vacancy_by_salary(pay_size):
    pay_query = { "$or": [ { "min_salary": {"$lte": pay_size }, "max_salary": None },
                         { "min_salary": {"$lte": pay_size }, "max_salary": {"$gt": pay_size } },
                         { "min_salary": None, "max_salary": { "$gt": pay_size } }
                        ] }
    amount_of_vacancies = 0
    for vacancy in vacancies_collection.find(pay_query):
        print(vacancy)
        amount_of_vacancies += 1
    return amount_of_vacancies

print("На экран будут выведены вакансии с заработной платой выше введённой суммы.")
entered_salary = int(input("Введите сумму: "))
print(search_vacancy_by_salary(entered_salary))
