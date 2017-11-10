import json
import requests

from settings import config


def direct_text_message(text, sender='1152791091497391'):
    params = {"access_token": config.PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    r_dict = {
        "recipient": {
            "id": sender
        },
        "message": {
                        'quick_replies': [{
                            'content_type': 'text',
                            'payload': 'financial_advice',
                            'title': 'Advises'
                        },
                            {
                                'content_type': 'text',
                                'payload': 'show_stocks',
                                'title': 'Stocks'
                            },
                            {
                                'content_type': 'text',
                                'payload': 'more_options',
                                'title': 'More options'
                            }],
                        'text': text
                    }
    }

    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                  params=params,
                  headers=headers,
                  data=json.dumps(r_dict))
    return r
