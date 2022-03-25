import logging
import json
from itertools import dropwhile

from flask import Flask, request

from utils import translate


app = Flask(__name__)

description = """
Привет! Я могу получить перевод слова.

Например:
Пользователь: Переведи слово стакан
Алиса: glass
"""


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    if req['session']['new']:
        res['response']['text'] = description
        return
    ttt = get_text_to_translate(req)
    if not ttt:
        res['response']['text'] = f'А что переводить то?'
    else:
        translated = translate(ttt, "ru", "en")
        res['response']['text'] = translated


def get_text_to_translate(req):
    text_to_translate = dropwhile(lambda x: x != "слово", req["request"]["nlu"]["tokens"])
    next(text_to_translate)
    return " ".join(text_to_translate)


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)