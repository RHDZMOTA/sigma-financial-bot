import json
import requests
from settings import config

LOCAL_URL = "http://localhost:8080/fb-messenger/sigma-bot"


def test_simple_get_request(url):
    return requests.get(url).text


def generate_example_text(text):
    return {
        'object': 'page',
        'entry': [{
            'id': '1152791091497391',
            'messaging': [{
                'message': {
                    'seq': 215641,
                    'text': text,
                    'mid': 'mid.$cAABsAZUzq79k7ceQW1evIJBrvaFT'
                },
                'recipient': {'id': '118754562014506'},
                'timestamp': 1506401208411,
                'sender': {
                    'id': '1152791091497391'
                }
            }],
            'time': 1506401208640
        }]
    }


def send_text_message(text, sender_id='1152791091497391'):

    params = {"access_token": config.PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}

    r = requests.post(LOCAL_URL, # url_production, url_local
                        params=params,
                        headers=headers,
                        data=json.dumps(generate_example_text(text)))
    return r




text = "create portfolio BIMBO ALSEA"
txt_ex = generate_example_text(text)
r = send_text_message(text)
r.json()
