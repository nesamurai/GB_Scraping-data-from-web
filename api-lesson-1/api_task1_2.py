import json
import requests


link = "https://api.trello.com/1/members/me/"
myAPIKey = "37f13a43da398a79605bb8d83a338db5"
myAPIToken = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # It's not publicly available! I can't show it.

params = {
    "key": myAPIKey,
    "token": myAPIToken,
}

# An object containing information about my Trello user
response = requests.get(link, params=params)
user = response.json()

with open('trello_info.json', 'w', encoding='utf-8') as json_file:
    json.dump(user, json_file)


link_board = "https://api.trello.com/1/members/me/boards"
board_response = requests.get(link_board, params=params)
boards = board_response.json()
with open('trello_boards.json', 'w', encoding='utf-8') as json_file:
    json.dump(boards, json_file)


params = {
    "key": myAPIKey,
    "token": myAPIToken,
    "fields": ["name", "url"]
}

names_and_urls_response = requests.get(link_board, params=params)
names_and_urls = names_and_urls_response.json()
with open('boards_names_urls.json', 'w', encoding='utf-8') as json_file:
    json.dump(names_and_urls, json_file)


# Получение карточек на досках
link_card  = "https://api.trello.com/1/boards/6118fc50292bfd56d2b74a30/cards"

headers = {
   "Accept": "application/json"
}

query = {
    "key": myAPIKey,
    "token": myAPIToken,
}

cards_response = requests.get(link_card, headers=headers, params=query)
cards = cards_response.json()
with open('cards.json', 'w', encoding='utf-8') as json_file:
    json.dump(cards, json_file)
