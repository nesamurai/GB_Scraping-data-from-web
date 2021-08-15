import json
import requests


# для вывода репозиториев преподавателя по курсу "Алгоритмы" на гикбрейнс
link_teacher_repositories = "http://api.github.com/users/crane1983/repos"

# для вывода моих репозиториев
link_mine_repositories = "http://api.github.com/users/nesamurai/repos"

headers = {"User-Agent": "nesamurai"}
params = {"type": "owner"}

# информация по преподавателю
response_for_teacher = requests.get(link_teacher_repositories, params=params, headers=headers)
extracted_data_for_teacher = response_for_teacher.json()

with open('teacher_repos.json', 'w', encoding='utf-8') as json_file:
    json.dump(extracted_data_for_teacher, json_file)

for repo in extracted_data_for_teacher:
    print(repo['name'])

# информация по мне
print('*****************************************')
response_for_me = requests.get(link_mine_repositories, params=params, headers=headers)
extracted_data_for_me = response_for_me.json()

with open('my_repos.json', 'w', encoding='utf-8') as json_file:
    json.dump(extracted_data_for_me, json_file)

for repo in extracted_data_for_me:
    print(repo['name'])
