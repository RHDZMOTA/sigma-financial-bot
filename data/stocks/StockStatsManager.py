# -*- coding: utf-8 -*-
import json
import time
import requests

from util.base_model import SerializableModel, db
from util.custom_requests import get_request_json
#from google.appengine.api import urlfetch


#urlfetch.set_default_fetch_deadline(45)


#def get_request(url):
#    r = urlfetch.fetch(url=url, method='GET', deadline=40)
#    return json.loads(r.content)


class StockIndicatorModel(SerializableModel):
    created_at = db.DateTimeProperty(auto_now_add=True)
    unix_query = db.IntegerProperty(required=True)
    stock = db.StringProperty()
    text = db.StringProperty()
    price_earnings_ratio = db.StringProperty()
    price_book_value_ratio = db.StringProperty()
    earnings_per_share = db.StringProperty()
    book_value_per_share = db.StringProperty()
    shares_outstanding = db.StringProperty()


class StockMarketRatesModel(SerializableModel):
    created_at = db.DateTimeProperty(auto_now_add=True)
    unix_query = db.IntegerProperty(required=True)
    stock = db.StringProperty()
    text = db.StringProperty()
    date = db.StringProperty()
    ask_vol = db.StringProperty()
    ask_price = db.StringProperty()
    bid_vol = db.StringProperty()
    bid_price = db.StringProperty()
    last_trade_price = db.StringProperty()
    prev_price = db.StringProperty()
    change = db.StringProperty()
    traded_vol = db.StringProperty()
    max_price = db.StringProperty()
    min_price = db.StringProperty()


class StockStatsManger(object):
    def __init__(self, stock):
        self.url = "https://bmv-info-api.herokuapp.com/stocks/statistics/" + stock.upper()
        self.epoch_time = int(time.time())
        self.stock = stock.upper()

    def get_from_web(self):
        statistical_api = self.url

        def get_statistics(limit=5):
            if True:
                return get_request_json(statistical_api)
            try:
                #r = requests.get(statistical_api)
                #res = r.json()
                res = get_request_json(statistical_api)
                return res
            except:
                if limit:
                    return get_statistics(limit - 1)
                return {"service_not_available": "Service not available"}

        statistics = get_statistics(limit=5)
        return statistics

    def save(self, stats):
        if "service_not_available" in stats:
            return None
        StockIndicatorModel(
            unix_query=self.epoch_time,
            stock=self.stock,
            text=stats["stock_indicators"].get("text"),
            price_earnings_ratio=stats["stock_indicators"].get("price_earnings_ratio"),
            price_book_value_ratio=stats["stock_indicators"].get("price_book_value_ratio"),
            earnings_per_share=stats["stock_indicators"].get("earnings_per_share"),
            book_value_per_share=stats["stock_indicators"].get("book_value_per_share"),
            shares_outstanding=stats["stock_indicators"].get("shares_outstanding")
        ).build()

        StockMarketRatesModel(
            unix_query=self.epoch_time,
            stock=self.stock,
            text=stats["stock_market_rates"].get("text"),
            date=stats["stock_market_rates"].get("date"),
            ask_vol=stats["stock_market_rates"].get("ask_vol"),
            ask_price=stats["stock_market_rates"].get("ask_price"),
            bid_vol=stats["stock_market_rates"].get("bid_vol"),
            bid_price=stats["stock_market_rates"].get("bid_price"),
            last_trade_price=stats["stock_market_rates"].get("last_trade_price"),
            prev_price=stats["stock_market_rates"].get("prev_price"),
            change=stats["stock_market_rates"].get("change"),
            traded_vol=stats["stock_market_rates"].get("traded_vol"),
            max_price=stats["stock_market_rates"].get("max_price"),
            min_price=stats["stock_market_rates"].get("min_price")
        ).build()

    def get_or_create(self):
        query_sim = StockIndicatorModel.query(
            StockIndicatorModel.unix_query > self.epoch_time - 2 * 60 * 60,
            StockIndicatorModel.stock == self.stock
        ).fetch(limit=1)
        query_smr = StockMarketRatesModel.query(
            StockMarketRatesModel.unix_query > self.epoch_time - 2 * 60 * 60,
            StockMarketRatesModel.stock == self.stock
        ).fetch(limit=1)
        if len(query_sim) and len(query_smr):
            return {
                "stock_id": self.stock,
                "stock_indicators": query_sim[0].to_dict(),
                "stock_market_rates": query_smr[0].to_dict()
            }
        stats = self.get_from_web()
        self.save(stats)
        return stats