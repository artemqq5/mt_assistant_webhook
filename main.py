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
COMMENT_TASK = "action_comment_on_card"
ADD_NEW_TASK = "action_create_card"

TASK_DONE = "on_approve"
TASK_ACTIVE = "active"

# webhok for tech List new task TEST
# 65ae8a93749840a80db66415 webhok for tech List new task PROD

# webhok for creo List new task TEST
# 65b3842454c6b836d995d47c webhok for creo List new task TEST


@app.route('/webhook', methods=['POST', 'GET'])
def webhook_handler():
    if request.method == 'POST':
        try:
            data = request.json
            # print(data)
            model = parse_trello_response(data)
            print(str(model))

            # змінили статус завданню на дошці CREO
            if model.translationKey == CHANGE_STATUS_TASK:
                if model.customFieldItemIdValue == COMPLETED_STATUS_TRELLO:
                    print("змінили статус завданню на дошці CREO -> creo done")
                    status_task = "готово 🟢"
                    task_change_status_notify(id_card=model.id, table_name='cards_creo', name=model.name,
                                              url=model.shortUrl,
                                              status=status_task)
                elif model.customFieldItemIdValue == ACTIVE_STATUS_TRELLO:
                    print("змінили статус завданню на дошці CREO -> creo active")
                    status_task = "в процесі 🟠️"
                    task_change_status_notify(id_card=model.id, table_name='cards_creo', name=model.name,
                                              url=model.shortUrl,
                                              status=status_task)
            # перемістили завдання в колонку готово (технічка)
            elif model.translationKey == MOVE_TASK:
                if model.listAfterId == list_tech_done:
                    print("перемістили завдання в колонку готово (технічка)")
                    task_done_notify(id_card=model.id, table_name='cards_tech', name=model.name, url=model.shortUrl)
            # Залишили коммент до завдання в трелло
            elif model.translationKey == COMMENT_TASK:
                if model.webhook_name == 'Creo':
                    print("Залишили коммент до завдання в трелло (creo)")
                    comment_task_notify(table_name='cards_creo', name=model.name, url=model.shortUrl,
                                        comment=model.comment)

                elif model.webhook_name == 'Tech':
                    print("Залишили коммент до завдання в трелло (технічка)")
                    comment_task_notify(table_name='cards_tech', name=model.name, url=model.shortUrl,
                                        comment=model.comment)
            # Створили нове завдання з трелло (не через бота) в список технічки
            elif model.translationKey == ADD_NEW_TASK and not model.name.startswith('#'):
                if model.idList == list_from_tech:
                    print("tech new task add from trello (no bot)")
                    new_task_no_bot(table_name='cards_tech',  name=model.name, url=model.shortUrl)
                elif model.idList == list_from_creo:
                    print("creo new task add from trello (no bot)")
                    new_task_no_bot(table_name='cards_creo', name=model.name, url=model.shortUrl)

            # Інша операція
            else:
                print("none model")

        except Exception as e:
            print(f"error: {e}")
    else:
        print("GET")

    return "OK", 200


def parse_trello_response(data):
    # Безпечне отримання значень з використанням get()
    customFieldItem = data.get('action', {}).get('data', {}).get('customFieldItem')

    # Ініціалізація змінних з перевіркою на None
    customFieldItemIdValue = customFieldItem.get('idValue', None) if customFieldItem else None

    listAfter = data.get('action', {}).get('data', {}).get('listAfter')
    listAfterId = listAfter.get('id', None) if listAfter else None
    listAfterText = listAfter.get('name', None) if listAfter else None

    commentData = data.get('action', {}).get('data', {})
    comment = commentData.get('text', None) if commentData else None

    model = data.get('model', {})
    id_ = model.get('id', None)
    desc = model.get('desc', None)
    idBoard = model.get('idBoard', None)
    idList = data.get('action', {}).get('display', {}).get("entities", {}).get("list", {}).get("id", {})
    name = data.get('action', {}).get('data', {}).get('card', {}).get('name', None)
    shortUrl = data.get('action', {}).get('data', {}).get('card', {}).get('shortLink', None)

    actionDisplay = data.get('action', {}).get('display', {})
    translationKey = actionDisplay.get('translationKey', None)

    webhookData = data.get('webhook', {})
    webhookName = webhookData.get('description', '').split("_")[0] if webhookData else None

    return TrelloAction(
        id_=id_,
        desc=desc,
        idBoard=idBoard,
        idList=idList,
        name=name,
        shortUrl=f"https://trello.com/c/{shortUrl}",
        translationKey=translationKey,
        customFieldItemIdValue=customFieldItemIdValue,
        listAfterId=listAfterId,
        listAfterText=listAfterText,
        comment=comment,
        webhook_name=webhookName
    )


def task_done_notify(id_card, table_name, name, url):
    try:
        id_user = MyDatabase().get_id_user_by_card_id(table_name, id_card)
        if id_user is not None:
            json_data_pass = {
                "chat_id": id_user,
                "parse_mode": "html",
                "text": f"<b>{name}</b>\n\nЗадача позначена як виконана 🟢\n\n{url}"
            }
            requests.request(method='POST', url=URL_MESSAGE, data=json_data_pass)
    except Exception as e:
        print(f"task_done_notify: {e}")


def task_change_status_notify(id_card, table_name, name, url, status):
    try:
        id_user = MyDatabase().get_id_user_by_card_id(table_name, id_card)
        if id_user is not None:
            json_data_pass = {
                "chat_id": id_user,
                "parse_mode": "html",
                "text": f"<b>{name}</b>\n\nЗадача змінили статус на {status}!\n\n{url}"
            }
            requests.request(method='POST', url=URL_MESSAGE, data=json_data_pass)
    except Exception as e:
        print(f"task_change_status_notify: {e}")


def comment_task_notify(table_name, name, url, comment):
    try:
        dep = 'designer' if table_name == 'cards_creo' else 'tech'
        users = MyDatabase().get_users_by_dep(dep)
        if users is not None:
            for user in users:
                json_data_pass = {
                    "chat_id": user['id_user'],
                    "parse_mode": "html",
                    "text": f"<b>Новий коментар до задачі!</b>\n{name}\n\n{comment}\n\n{url}"
                }
                requests.request(method='POST', url=URL_MESSAGE, data=json_data_pass)

    except Exception as e:
        print(f"comment_task_notify: {e}")


def new_task_no_bot(table_name, name, url):
    try:
        dep = 'designer' if table_name == 'cards_creo' else 'tech'
        users = MyDatabase().get_users_by_dep(dep)
        if users is not None:
            for user in users:
                json_data_pass = {
                    "chat_id": user['id_user'],
                    "parse_mode": "html",
                    "text": f"<b>Нова задача! (поставлена не через бот)</b>\n{name}\n\n{url}"
                }
                requests.request(method='POST', url=URL_MESSAGE, data=json_data_pass)

    except Exception as e:
        print(f"new_task_no_bot: {e}")

#


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
