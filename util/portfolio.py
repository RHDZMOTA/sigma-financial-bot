
from util.custom_requests import get_request_json, get_request_content


BMV_PORTFOLIO_API = "https://bmv-portfolio-api.herokuapp.com"
BMV_SHAPE = "/sharpe/create?stocks={stocks}"
BMV_MARKOWITZ = "/markowitz/create?stocks={stocks}&percentile={perc}"


#import requests
#def get_request_json(url):
#    return requests.get(url).json()

class PortfolioManager(object):

    def __init__(self, stocks):
        self.stocks = stocks

    def get_sharpe(self):
        try:
            resp = get_request_json(BMV_PORTFOLIO_API + BMV_SHAPE.format(stocks=str(self.stocks)))
        except:
            resp = {"Error": "Unable to reach sharpe-portfolio-creation service."}
        return resp

    def get_markowitz(self, percentile):
        def validate_percetile(x):
            return 0 < float(x) and float(x) < 100
        if not validate_percetile(percentile):
            return {"Error": "Percentile not valid."}
        #resp = get_request_json(BMV_PORTFOLIO_API + BMV_MARKOWITZ.format(stocks=str(self.stocks), perc=str(percentile)))
        try:
            #resp = get_request_json(BMV_PORTFOLIO_API + BMV_MARKOWITZ.format(stocks=str(self.stocks), perc=str(percentile)))
            resp = get_request_content(BMV_PORTFOLIO_API + BMV_MARKOWITZ.format(stocks=str(self.stocks), perc=str(percentile)))
        except:
            resp = "Error: Unable to reach markowitz-portfolio-creation service."#{"Error": "Unable to reach markowitz-portfolio-creation service."}
        return resp


#portfolio_manager = PortfolioManager(["ALSEA", "GRUMAB"])
#portfolio_manager.get_sharpe()
#portfolio_manager.get_markowitz(percentile=99)

