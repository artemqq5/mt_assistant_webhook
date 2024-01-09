import json
import re

import pymysql
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from trello import TrelloClient
import requests

from cfg.config import API_KEY_TRELLO, API_SECRET_TRELLO, TOKEN_TRELLO, CONNECTION_PASSWORD, DB_NAME, list_from_creo, \
    list_from_tech, URL_MESSAGE, COMPLETED_STATUS_TRELLO, ACTIVE_STATUS_TRELLO, list_tech_done
from repository.database_ import MyDatabase
from repository.trello_ import TrelloAction

app = Flask(__name__)

CHANGE_STATUS_TASK = "action_update_custom_field_item"
MOVE_TASK = "action_move_card_from_list_to_list"

TASK_DONE = "on_approve"
TASK_ACTIVE = "active"


@app.route('/webhook', methods=['POST', 'GET'])
def webhook_handler():
    if request.method == 'POST':
        try:
            data = request.json
            model = parse_trello_response(data)

            if model.translationKey == CHANGE_STATUS_TASK:
                if model.customFieldItemIdValue == COMPLETED_STATUS_TRELLO:
                    print("creo done")
                    status_task = "готово 🟢"
                    task_change_status(id_card=model.id, table_name='cards_creo', name=model.name, url=model.shortUrl,
                                       status=status_task)
                elif model.customFieldItemIdValue == ACTIVE_STATUS_TRELLO:
                    print("creo in active")
                    status_task = "в процесі 🟠️"
                    task_change_status(id_card=model.id, table_name='cards_creo', name=model.name, url=model.shortUrl,
                                       status=status_task)
            elif model.translationKey == MOVE_TASK:
                if model.listAfterId == list_tech_done:
                    print("Задача з tech в Готово")
                    task_done_(id_card=model.id, table_name='cards_tech', name=model.name, url=model.shortUrl)
            else:
                pass

        except Exception as e:
            print(f"error: {e}")
    else:
        print("GET")

    return "OK", 200


def parse_trello_response(data):
    customFieldItem = data['action']['data'].get('customFieldItem', None)

    if customFieldItem is not None:
        customFieldItemIdValue = customFieldItem.get('idValue', None)
    else:
        customFieldItemIdValue = None

    # Check if 'listAfter' exists and is not None
    listAfter = data['action']['data'].get('listAfter')
    if listAfter:
        listAfterId = listAfter.get('id', None)
        listAfterText = listAfter.get('name', None)
    else:
        listAfterId = None
        listAfterText = None

    return TrelloAction(
        id_=data['model']['id'],
        desc=data['model']['desc'],
        idBoard=data['model']['idBoard'],
        idList=data['model']['idList'],
        name=data['model']['name'],
        shortUrl=data['model']['shortUrl'],
        translationKey=data['action']['display']['translationKey'],
        customFieldItemIdValue=customFieldItemIdValue,
        listAfterId=listAfterId,
        listAfterText=listAfterText
    )


def task_done_(id_card, table_name, name, url):
    try:
        id_user = MyDatabase().get_id_user_by_card_id(table_name, id_card)
        # print(id_user)
        if id_user is not None:
            json_data_pass = {
                "chat_id": id_user,
                "parse_mode": "html",
                "text": f"<b>{name}</b>\n\nЗадача позначена як виконана 🟢\n\n{url}"
            }
            result = requests.request(method='POST', url=URL_MESSAGE, data=json_data_pass)
            # print(result.json())
    except Exception as e:
        print(f"done_task(id_card, table_name): {e}")


def task_change_status(id_card, table_name, name, url, status):
    try:
        id_user = MyDatabase().get_id_user_by_card_id(table_name, id_card)
        # print(id_user)
        if id_user is not None:
            json_data_pass = {
                "chat_id": id_user,
                "parse_mode": "html",
                "text": f"<b>{name}</b>\n\nЗадача змінили статус на {status}!\n\n{url}"
            }
            result = requests.request(method='POST', url=URL_MESSAGE, data=json_data_pass)
            # print(result.json())
    except Exception as e:
        print(f"done_task(id_card, table_name): {e}")


# change status card 1
# 'id': '659d6bfe39ed5284f27144fb'
# 'desc': 'offers_name: test\ndesc: test\n\nusername: @artem\ntelegram id: 886327182\n'
# 'idBoard': '657349bfd5dd7da8739e6058'
# 'idList': '658bdfb79109634c42cdfb7c'
# 'name': '#108 Припаркувати домен 🅿️'
# 'shortUrl': 'https://trello.com/c/CpS48Ca3'
# 'customFieldItem': 'idValue': '65734c7eeed58843d579f08a'
# 'name': 'TEST FOR DEVELOPMENT BOT'
# 'display': {'translationKey': 'action_update_custom_field_item',

# move card 1
# {'model': {'id': '659d6bfe39ed5284f27144fb',
# 'desc': 'offers_name: test\ndesc: test\n\nusername: @artem\ntelegram id: 886327182\n',
# 'idBoard': '657349bfd5dd7da8739e6058',
# 'idList': '658be90aa17b85c39e0bb722',
# 'name': '#108 Припаркувати домен 🅿️',
# shortUrl': 'https://trello.com/c/CpS48Ca3',
# 'display': {'translationKey': 'action_moved_card_higher', action_moved_card_lower action_move_card_from_list_to_list
# 'listAfter': {'type': 'list', 'id': '658be90aa17b85c39e0bb722', 'text': 'DONE TECH'}


if __name__ == '__main__':
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()
    # app.run()
