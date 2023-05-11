from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
import requests
import json

from private_config import local_telegram_token, server_telegram_token, list_tech_done_local, list_creo_done_local, \
    list_tech_done, list_creo_done

app = Flask(__name__)

DEBUG_MODE = True

if DEBUG_MODE:
    URL_MESSAGE = f"https://api.telegram.org/bot{local_telegram_token}/sendMessage"
    list_tech = list_tech_done_local
    list_creo = list_creo_done_local
else:
    URL_MESSAGE = f"https://api.telegram.org/bot{server_telegram_token}/sendMessage"
    list_tech = list_tech_done
    list_creo = list_creo_done


@app.route('/webhook', methods=['POST', 'GET'])
def webhook_handler():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(data)

            if data['action']['data']['card']['idList'] == list_creo:
                print('creative')
            elif data['action']['data']['card']['idList'] == list_tech:
                print('tech')

            card_label = data['action']['data']['card']['name']
            card_id = data['action']['data']['card']['id']

            jsonDataPass = {
                "chat_id": "6002568864",
                "text": f"{card_label} | {card_id}"
            }
            headers = {
                "Content-Type": "application/json"
            }
            result = requests.post(URL_MESSAGE, json.dumps(jsonDataPass), headers)
            print(result.status_code)

            print(card_label)
            print(card_id)
        except Exception as e:
            print("exception when getting data POST")
            print(f"exception {e}")
    else:
        print("get request success GET")

    return 'OK', 200


if __name__ == '__main__':
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()
