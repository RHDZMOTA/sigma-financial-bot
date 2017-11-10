# -*- coding: utf-8 -*-
import json
import requests

from data.stocks.StockStatsManager import StockStatsManger
from data.stocks.prices import get_symbol_data, suggestion_strategy


def get_descriptions():
    with open("data/stocks/description.json") as file:
        desc = json.load(file)
    return desc


def get_stock_categorical_desc(stock):
    return get_descriptions().get(stock)


def get_stock_statistical_desc(stock):
    return StockStatsManger(stock).get_or_create()
    #statistical_api = "https://bmv-info-api.herokuapp.com/stocks/statistics/" + stock.upper()
    #
    #def get_statistics(limit=5):
    #    try:
    #        return requests.get(statistical_api).json()
    #    except:
    #        if limit:
    #            return get_statistics(limit-1)
    #        return {"service_not_available": "Service not available"}
    #statistics = get_statistics(limit=5)
    #return statistics


def get_stock_desc(stock):
    categ = get_stock_categorical_desc(stock)
    return {
        "categorical": categ,
        "statistical": get_stock_statistical_desc(categ.get("bmv_id"))
    }


def get_tickers():
    return list(get_descriptions().keys())


def get_symbol(stock):
    return stock + get_descriptions().get(stock).get("main_serie")
