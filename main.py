import pymysql
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from trello import TrelloClient
import requests

from config import DEBUG_MODE
from private_config import *

app = Flask(__name__)

if DEBUG_MODE:
    URL_MESSAGE = f"https://api.telegram.org/bot{local_telegram_token}/sendMessage"
    list_tech = list_tech_done_local
    list_creo = list_creo_done_local
    list_from_tech = idList_tech_test
    list_from_creo = idList_creo_test
    API_KEY_TRELLO = server_api_key_trello
    TOKEN_TRELLO = server_token_trello
    API_SECRET_TRELLO = server_secret_trello
    CONNECTION_PASSWORD = local_password_connection
    DB_NAME = local_name_db
else:
    URL_MESSAGE = f"https://api.telegram.org/bot{server_telegram_token}/sendMessage"
    list_tech = list_tech_done
    list_creo = list_creo_done
    list_from_tech = idList_tech
    list_from_creo = idList_creo
    API_KEY_TRELLO = server_api_key_trello
    TOKEN_TRELLO = server_token_trello
    API_SECRET_TRELLO = server_secret_trello
    CONNECTION_PASSWORD = server_password_connection
    DB_NAME = server_name_db

clientTrelloApi = TrelloClient(
    api_key=API_KEY_TRELLO,
    api_secret=API_SECRET_TRELLO,
    token=TOKEN_TRELLO
)


def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password=CONNECTION_PASSWORD,
        db=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route('/webhook', methods=['POST', 'GET'])
def webhook_handler():
    if request.method == 'POST':
        try:
            data = request.get_json()
            action = data['action']['display']['translationKey']
            card = data['action']['display']['entities']['card']
            list_after = data['action']['display']['entities'].get('list') if 'list' in data['action']['display'][
                'entities'] else data['action']['display']['entities'].get('listAfter')

            id_of_list_after = list_after['id']

            print(f"{data}\n\n\n\n")
            print(f"{action}\n\n")
            print(f"{list_after}\n\n")

            if id_of_list_after == list_creo:
                print("Done creo")
                done_task(id_card=card["id"], table_name="cards_creo")
            elif id_of_list_after == list_tech:
                print("Done tech")
                done_task(id_card=card["id"], table_name="cards_tech")
            elif id_of_list_after in (list_from_creo,):
                if action == "action_create_card":
                    print("Create creo")
                    create_task(id_card=card["id"], dep="designer", sub_text="Нова задача")
                else:
                    print("move to creo new")
                    create_task(id_card=card["id"], dep="designer", sub_text="Задание вернулось в колонку")
            elif id_of_list_after in (list_from_tech,):
                if action == "action_create_card":
                    print("Create tech")
                    create_task(id_card=card["id"], dep="tech", sub_text="Нова задача")
                else:
                    print("move to tech new")
                    create_task(id_card=card["id"], dep="tech", sub_text="Задание вернулось в колонку")
            else:
                print("None")

        except Exception as e:
            print("exception when getting data POST")
            print(f"exception {e}")
    else:
        print("get request success GET")

    return 'OK', 200


def create_task(id_card, dep, sub_text):
    try:
        card = clientTrelloApi.get_card(id_card)
        users = get_users_from_db(dep)
        for user in users:
            json_data_pass = {"chat_id": user, "text": f"{card.name} - {sub_text} 🔨 \n{card.url}"}
            result = requests.request(method='POST', url=URL_MESSAGE, data=json_data_pass)
            print(result.status_code)
    except Exception as e:
        print(f"create_task(id_card, table_name): {e}")


def done_task(id_card, table_name):
    try:
        card = clientTrelloApi.get_card(id_card)
        result = get_card_from_db(table_name, id_card)
        if result is not None:
            json_data_pass = {
                "chat_id": result[0],
                "text": f"{card.name} - Задачу виконано 👌 \n{card.url}"
            }
            result = requests.request(method='POST', url=URL_MESSAGE, data=json_data_pass)
            print(result.status_code)
    except Exception as e:
        print(f"done_task(id_card, table_name): {e}")


def get_card_from_db(table_name, id_card):
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                select_card = f"SELECT `id_user` FROM `{table_name}` WHERE `id_card` = '{id_card}';"

                cursor.execute(select_card)
                result = [cursor.fetchall()[0]['id_user']]

            connection.commit()
            return result
    except Exception as e:
        print(f"get_card_from_db() {e}")
        return None


def get_users_from_db(dep):
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                select_user = f"SELECT * FROM `users` WHERE `dep_user` = '{dep}';"

                cursor.execute(select_user)
                result = []

                for i in cursor.fetchall():
                    result.append(i['id_user'])

                print(f"all users {dep}: {result}")

            connection.commit()
            return result
    except Exception as e:
        print(f"get_users_from_db() {e}")
        return None


if __name__ == '__main__':
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()
    # app.run()
