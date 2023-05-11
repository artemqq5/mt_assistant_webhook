from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
import requests
import json

from private_config import local_telegram_token, server_telegram_token, list_tech_done_local, list_creo_done_local, \
    list_tech_done, list_creo_done

app = Flask(__name__)

DEBUG_MODE = False

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
        data = request.get_json()

    # data_message = {
    #     "chat_id": chat_id,
    #     "text": text
    # }
    # requests.request('POST', URL_MESSAGE, data_message)

    else:
        data = "get request success"

    print(data)
    return 'OK', 200


if __name__ == '__main__':
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()
