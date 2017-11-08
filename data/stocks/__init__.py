import json


def get_descriptions():
    with open("data/stocks/mexican_tickers.json") as file:
        stocks = json.load(file)
    return stocks


def get_tickers():
    return list(get_descriptions().keys())
