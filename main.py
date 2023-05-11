from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
import requests
import json

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook_handler():
    data = request.get_json() or request.form.to_dict()

    print(data)
    return 'OK', 200


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()
