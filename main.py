from flask import Flask, request
from gevent.pywsgi import WSGIServer

from private_config import *
from private_config import GLEB_ID, EGOR_ID, ID_LIST_TECH_GLEB, ID_LIST_TECH_EGOR, ID_LIST_TECH_NEW, ID_LIST_CREO_NEW, \
    COMPLETED_STATUS_TRELLO, ACTIVE_STATUS_TRELLO, ID_LIST_TECH_DONE
from repository.MainRepository import MainRepository
from repository.usecase.NotificationCreo import NotificationCreo
from repository.usecase.NotificationTech import NotificationTech
from repository.usecase.TrelloParser import TrelloParser

app = Flask(__name__)

CHANGE_STATUS_TASK = "action_update_custom_field_item"
MOVE_TASK = "action_move_card_from_list_to_list"
COMMENT_TASK = "action_comment_on_card"
ADD_NEW_TASK = "action_create_card"

WEBHOOK_TECH = "TechNew"

TASK_DONE = "on_approve"
TASK_ACTIVE = "active"


@app.route('/webhook', methods=['POST', 'GET'])
def webhook_handler():
    if request.method == 'POST':
        try:
            data = request.json
            # print(data)
            model = TrelloParser.parse_trello_response(data)
            print(str(model))

            # print(model.translationKey == CHANGE_STATUS_TASK)
            # print(model.customFieldItemIdValue == COMPLETED_STATUS_TRELLO)

            # Створили нове завдання з трелло (не через бота)
            if model.translationKey == ADD_NEW_TASK and not model.name.startswith('#'):
                # технічка
                if model.idList == ID_LIST_TECH_GLEB:
                    print("tech new task add from trello gleb (no bot)")
                    NotificationTech().new_task_no_bot(name=model.name, url=model.shortUrl, id_user=[GLEB_ID])
                elif model.idList == ID_LIST_TECH_EGOR:
                    print("tech new task add from trello egor (no bot)")
                    NotificationTech().new_task_no_bot(name=model.name, url=model.shortUrl, id_user=[EGOR_ID])
                elif model.idList == ID_LIST_TECH_NEW:
                    print("tech new task add from trello all (no bot)")
                    NotificationTech().new_task_no_bot(name=model.name, url=model.shortUrl, id_user=[EGOR_ID, GLEB_ID])
                # крео
                elif model.idList == ID_LIST_CREO_NEW:
                    print("creo new task add from trello (no bot)")
                    NotificationCreo().new_task_no_bot(name=model.name, url=model.shortUrl)
            elif model.webhook_name == WEBHOOK_TECH:
                print(f"Double webhook from: {model.webhook_name} was skipped")
                return "Error", 400

            # змінили статус завданню на дошці CREO
            elif model.translationKey == CHANGE_STATUS_TASK:
                if model.customFieldItemIdValue == COMPLETED_STATUS_TRELLO:
                    print("змінили статус завданню на дошці CREO -> creo done")
                    status_task = "готово 🟢"
                    NotificationCreo().task_change_status(
                        id_card=model.id,
                        name=model.name,
                        url=model.shortUrl,
                        status=status_task
                    )
                elif model.customFieldItemIdValue == ACTIVE_STATUS_TRELLO:
                    print("змінили статус завданню на дошці CREO -> creo active")
                    status_task = "в процесі 🟠️"
                    NotificationCreo().task_change_status(
                        id_card=model.id,
                        name=model.name,
                        url=model.shortUrl,
                        status=status_task
                    )

            # перемістили завдання в колонку готово (технічка)
            elif model.translationKey == MOVE_TASK and model.listAfterId == ID_LIST_TECH_DONE:
                print("перемістили завдання в колонку готово (технічка)")
                NotificationTech().task_done(id_card=model.id, name=model.name, url=model.shortUrl)
            # перемістили завдання в колонку в процессі (технічка)
            elif model.translationKey == MOVE_TASK and model.listAfterId == ID_LIST_TECH_IN_PROCESS:
                print("перемістили завдання в колонку в процесі (технічка)")
                NotificationTech().task_in_proccess(id_card=model.id, name=model.name, url=model.shortUrl)
            # перемістили завдання в колонку new (технічка)
            elif model.translationKey == MOVE_TASK and (
                    model.listAfterId == ID_LIST_TECH_GLEB or model.listAfterId == ID_LIST_TECH_EGOR):
                print("перемістили завдання в колонку new (технічка)")
                NotificationTech().task_wait(id_card=model.id, name=model.name, url=model.shortUrl)
            # Залишили коммент до завдання в трелло
            elif model.translationKey == COMMENT_TASK:
                if model.webhook_name == 'creo':
                    print("Залишили коммент до завдання в трелло (creo)")
                    NotificationCreo().comment_task(name=model.name, url=model.shortUrl, comment=model.comment)
                elif model.webhook_name == 'tech':
                    print("Залишили коммент до завдання в трелло (технічка)")
                    card = MainRepository().tech_by_card_id(model.id)
                    if card['tech'] == "Gleb":
                        NotificationTech().comment_task(
                            name=model.name,
                            url=model.shortUrl,
                            comment=model.comment,
                            users=[GLEB_ID]
                        )
                    elif card['tech'] == "Egor":
                        NotificationTech().comment_task(
                            name=model.name,
                            url=model.shortUrl,
                            comment=model.comment,
                            users=[EGOR_ID]
                        )
                    elif model.idList == ID_LIST_TECH_NEW:
                        NotificationTech().comment_task(
                            name=model.name,
                            url=model.shortUrl,
                            comment=model.comment,
                            users=[EGOR_ID, GLEB_ID]
                        )
            else:
                print("else")
        except Exception as e:
            print(f"error: {e}")
    else:
        print("GET")

    return "OK", 200


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
