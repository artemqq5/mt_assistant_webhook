from flask import Flask, request
from gevent.pywsgi import WSGIServer
from trello import TrelloClient
import requests

from private_config import local_telegram_token, server_telegram_token, list_tech_done_local, list_creo_done_local, \
    list_tech_done, list_creo_done, idList_creo_test, idList_tech_test, idList_tech, idList_creo, local_api_key_trello, \
    local_token_trello, local_secret_trello, server_api_key_trello, server_token_trello, server_secret_trello

app = Flask(__name__)

DEBUG_MODE = True

if DEBUG_MODE:
    URL_MESSAGE = f"https://api.telegram.org/bot{local_telegram_token}/sendMessage"
    list_tech = list_tech_done_local
    list_creo = list_creo_done_local
    list_from_tech = idList_tech_test
    list_from_creo = idList_creo_test
    API_KEY_TRELLO = local_api_key_trello
    TOKEN_TRELLO = local_token_trello
    API_SECRET_TRELLO = local_secret_trello
else:
    URL_MESSAGE = f"https://api.telegram.org/bot{server_telegram_token}/sendMessage"
    list_tech = list_tech_done
    list_creo = list_creo_done
    list_from_tech = idList_tech
    list_from_creo = idList_creo
    API_KEY_TRELLO = server_api_key_trello
    TOKEN_TRELLO = server_token_trello
    API_SECRET_TRELLO = server_secret_trello

clientTrelloApi = TrelloClient(
    api_key=API_KEY_TRELLO,
    api_secret=API_SECRET_TRELLO,
    token=TOKEN_TRELLO
)


@app.route('/webhook', methods=['POST', 'GET'])
def webhook_handler():
    if request.method == 'POST':
        try:
            data = request.get_json()

            if data['action']['data']['card']['idList'] in (list_creo, list_tech):
                if data['action']['data']['listBefore']['id'] in (list_from_creo, list_from_tech):
                    card_id = data['action']['data']['card']['id']
                    get_card(card_id)

        except Exception as e:
            print("exception when getting data POST")
            print(f"exception {e}")
    else:
        print("get request success GET")

    return 'OK', 200


def get_card(id_card):
    # jsonDataPass = {
    #     "chat_id": "6002568864",
    #     "text": f"{'card_label'} | {'card_id'}"
    # }
    card = clientTrelloApi.get_card(id_card)
    print(card.name)
    print(card.desc)
    print(card.id)

    # result = requests.request(method='POST', url=URL_MESSAGE, data=jsonDataPass)
    # print(result)


# class Card:
#     def __self__(self, ):

if __name__ == '__main__':
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()
