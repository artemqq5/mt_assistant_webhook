import pymysql
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from trello import TrelloClient
import requests

from private_config import local_telegram_token, server_telegram_token, list_tech_done_local, list_creo_done_local, \
    list_tech_done, list_creo_done, idList_creo_test, idList_tech_test, idList_tech, idList_creo, \
    local_api_key_trello, \
    local_token_trello, local_secret_trello, server_api_key_trello, server_token_trello, server_secret_trello, \
    local_password_connection, local_name_db, server_password_connection, server_name_db

app = Flask(__name__)

DEBUG_MODE = False

if DEBUG_MODE:
    URL_MESSAGE = f"https://api.telegram.org/bot{local_telegram_token}/sendMessage"
    list_tech = list_tech_done_local
    list_creo = list_creo_done_local
    list_from_tech = idList_tech_test
    list_from_creo = idList_creo_test
    API_KEY_TRELLO = local_api_key_trello
    TOKEN_TRELLO = local_token_trello
    API_SECRET_TRELLO = local_secret_trello
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

            print(action)
            print(data['model']['id'])
            # print(data)

            # if card has moved to column (DONE TASK)
            if data['model']['id'] in (list_tech, list_creo) and action == "action_move_card_from_list_to_list":
                card_id = data['action']['data']['card']['id']
                if data['action']['data']['listAfter']['id'] == list_tech:
                    get_card(card_id, "cards_tech")
                elif data['action']['data']['listAfter']['id'] == list_creo:
                    get_card(card_id, "cards_creo")

            # if card has created in column (NEW TASK)
            elif data['model']['id'] == list_from_tech and action == "action_create_card":
                card_id = data['action']['data']['card']['id']
                get_card(card_id, "cards_tech", tech=True)
            else:
                print('step1 cancel')
        except Exception as e:
            print("exception when getting data POST")
            print(f"exception {e}")
    else:
        print("get request success GET")

    return 'OK', 200


def get_card(id_card, table_name, tech=False):
    card = clientTrelloApi.get_card(id_card)
    result = get_tech_from_db() if tech else get_card_from_db(table_name, id_card)
    if result is not None:
        message = "Нова задача 🔨" if tech else "Задача готова ✅"
        jsonDataPass = {
            "chat_id": result,
            "text": f"{card.name} - {message} \n{card.url}"
        }
        result = requests.request(method='POST', url=URL_MESSAGE, data=jsonDataPass)
        print(result.status_code)


def get_card_from_db(table_name, id_card):
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                select_card = f"SELECT `id_user` FROM `{table_name}` WHERE `id_card` = '{id_card}';"

                cursor.execute(select_card)
                result = cursor.fetchall()[0]['id_user']

            connection.commit()
            return result
    except Exception as e:
        print(f"get_card_from_db() {e}")
        return None


def get_tech_from_db():
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                select_user = f"SELECT * FROM `users` WHERE `dep_user` = 'tech';"

                cursor.execute(select_user)
                result = cursor.fetchall()[0]['id_user']

            connection.commit()
            return result
    except Exception as e:
        print(f"get_tech_from_db() {e}")
        return None


if __name__ == '__main__':
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()
