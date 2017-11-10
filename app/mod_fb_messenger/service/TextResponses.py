# -*- coding: utf-8 -*-
import random
import requests

from app.mod_fb_messenger.model import ResponsePacket, SingleResponse
from data.stocks import get_tickers, get_stock_desc, get_stock_categorical_desc
from data.stocks import get_symbol, get_symbol_data, suggestion_strategy
from util.messages import direct_text_message
from util.portfolio import PortfolioManager
from util.string_operations import replace
from abc import ABCMeta, abstractmethod


class AbstractTextResponses:
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_response_packet(self, response_packet):
        pass

    @abstractmethod
    def get_response_packet(self):
        pass

    @abstractmethod
    def get_text(self):
        pass

    @abstractmethod
    def get_first_name(self):
        pass


class HelloMessages(AbstractTextResponses):
    __metaclass__ = ABCMeta

    @staticmethod
    def identify_greeting(text):
        text = str(text).lower()
        text = replace(text, ["1", "¡", "!", "¿", "?", "."], "")
        text = replace(text, ["é"], "e")
        return ("hola" in text) or ("que tal" == text.replace("é", "e")) or ("que onda" == text.replace("é", "e")) or \
               ("saludos" in text) or ("salu2" in text) or ("hi" == text) or ("hello" in text) or ("greeting"  in text)

    def hello_world(self):
        if self.identify_greeting(self.get_text()) and not self.get_response_packet():
            text_res = [
                'Hey there, fellow human.',
                'Whaaaats up, bro. ;)',
                'Greetings there. ' + self.get_first_name() + '.',
                'Yo Yo Yo! Keep it rolling ' + self.get_first_name() + '!',
                "Hola. Huh, I mean... Hello. :)"
            ]
            self.set_response_packet(
                ResponsePacket(
                    quick_reply_id="main_menu",
                    single_list=[
                        SingleResponse(
                            content=random.choice(text_res),
                            content_type="text",
                            complement_info="None"
                        )
                    ]
                )
            )


class PresentYourself(AbstractTextResponses):
    __metaclass__ = ABCMeta

    @staticmethod
    def identify_name_request(text):
        text = text.lower()
        text = replace(text, ["1", "¡", "!", "¿", "?", "."], "")
        text = replace(text, ["é"], "e")
        text = replace(text, ["á"], "a")
        return ("cual" in text and "nombre" in text) or ("como" in text and "llama" in text) or \
               ("what" in text and "name" in text)

    @staticmethod
    def identify_presentation(text):
        text = text.lower()
        text = replace(text, ["1", "¡", "!", "¿", "?", "."], "")
        text = replace(text, ["é"], "e")
        text = replace(text, ["á"], "a")
        return ("quien" in text and "eres" in text) or ("que" in text and "eres" in text)

    def name_yourself(self):
        if self.identify_name_request(self.get_text()):
            names = [
                "My name is Sigma, your personal financial assistant. :)",
                "I'm Sigma, a pleasure to meet you. ;)",
                "I'm Sigma of House of house Targaryen the one and true ruler of the Seven Kingdoms of Westeros. JK, I'm just a financial assistant. :)"
            ]
            res_list = [
                [
                    SingleResponse(
                        content=random.choice(names),
                        content_type="text",
                        complement_info="None"
                    ),
                    SingleResponse(
                        content="And you may be " + self.get_first_name() + ". Right? :o",
                        content_type="text",
                        complement_info="None"
                    )
                ],
                [
                    SingleResponse(
                        content=random.choice(names),
                        content_type="text",
                        complement_info="None"
                    )
                ]
            ]
            self.set_response_packet(
                ResponsePacket(
                    quick_reply_id="main_menu",
                    single_list=random.choice(res_list)
                )
            )

    def present_yourself(self):
        if self.identify_presentation(self.get_text()):
            presentation = "Hello {}! I'm Sigma, a relative young AI that can assist you in finance and related stuff.".format(self.get_first_name())
            self.set_response_packet(
                ResponsePacket(
                    quick_reply_id="main_menu",
                    single_list=[
                        SingleResponse(
                            content=presentation,
                            content_type="text",
                            complement_info="None"
                        )
                    ]
                )
            )


class AcceptMessages(AbstractTextResponses):
    __metaclass__ = ABCMeta

    @staticmethod
    def identify_affirmation(text):
        text = str(text).lower()
        text = replace(text, ["1", "¡", "!", "¿", "?", "."], "")
        text = replace(text, ["í"], "i")
        return ("yes" == text) or ("si" == text) or ("okay" == text) or ("ok" == text) or ("afirmativo" in text) or \
               ("sure" == text) or ("alright" == text) or ("yeah" in text) or ("okay" == text) or ("right" in text)

    @staticmethod
    def identify_negation(text):
        text = str(text).lower()
        text = replace(text, ["1", "¡", "!", "¿", "?", "."], "")
        text = replace(text, ["á"], "a")
        return ("no" == text) or ("nunca" == text) or ("jamas" == text) or ("never" == text) or ("nope" == text) or \
               ("hell no" == text)

    def accept(self):
        if self.identify_affirmation(self.get_text()) and not self.get_response_packet():
            text_res = [
                'Perfect!',
                'Okay ;)',
                'Great :)',
                'Totally, ' + self.get_first_name() + '!']
            self.set_response_packet(
                ResponsePacket(
                    quick_reply_id="main_menu",
                    single_list=[
                        SingleResponse(
                            content=random.choice(text_res),
                            content_type="text",
                            complement_info="None"
                        )
                    ]
                )
            )
        elif self.identify_negation(self.get_text()) and not self.get_response_packet():
            text_res = [
                'Got it!',
                'Alright ;)',
                'Yep :)',
                'Thats right, ' + self.get_first_name() + '!']
            self.set_response_packet(
                ResponsePacket(
                    quick_reply_id="main_menu",
                    single_list=[
                        SingleResponse(
                            content=random.choice(text_res),
                            content_type="text",
                            complement_info="None"
                        )
                    ]
                )
            )


class SearchStock(AbstractTextResponses):
    __metaclass__ = ABCMeta

    @staticmethod
    def search_stock_invoked(text):
        return "search stock " in text.lower()

    def search_stock(self):
        #def get_top(xs, n=10):
        #    xs = sorted(xs, reverse=True)
        #    return xs if len(xs) < n else [] if n == 0 else [xs[0]] + get_top(xs[1:], n - 1)
        def get_top_stocks(xs, n=5):
            vals = [x[0] for x in sorted(xs, reverse=True, key=lambda z: z[1])]
            return vals if len(vals) < n else vals[:n]
        if self.search_stock_invoked(self.get_text()):
            stock = self.get_text().split(" ")[-1].replace(";", "").replace(":", "").upper()
            stocks = get_tickers()
            stocks_score = [0]*len(stocks)
            for letter in stock:
                stocks_score = [score + val for score, val in zip(stocks_score, [letter in s for s in stocks])]
            stocks_score = [score * (float(len(stock)) / float(len(s))
                                     if len(s) > len(stock)
                                     else float(len(s)) / float(len(stock)))
                            for score, s in zip(stocks_score, stocks)]
            #probable_scores = get_top(stocks_score)
            #probable_stocks = [s for s, score in zip(stocks, stocks_score) if score in probable_scores]
            probable_stocks = get_top_stocks(list(zip(stocks, stocks_score)))
            self.set_response_packet(
                ResponsePacket(
                    quick_reply_id="main_menu",
                    single_list=[
                        SingleResponse(
                            content="You may be looking for: {}".format(", ".join(probable_stocks[:10])),
                            content_type="text",
                            complement_info="None"
                        )
                    ]
                )
            )


class CompanyHistory(AbstractTextResponses):
    __metaclass__ = ABCMeta

    HISTORY_LIMIT = 500

    @staticmethod
    def identify_company_history(text):
        text = text.lower().replace(".", "")
        try:
            return (("history" in text) or ("company" in text)) and (len(text.split(" ")) < 4)#(text.split(" ")[-1].upper() in get_tickers())
        except Exception as e:
            return False

    def company_history(self):
        if self.identify_company_history(self.get_text()):
            stock = self.get_text().split(" ")[-1].replace(".", "").replace(";", "").replace(":", "").upper()
            if stock not in get_tickers():
                self.set_response_packet(
                    ResponsePacket(
                        quick_reply_id="main_menu",
                        single_list=[
                            SingleResponse(
                                content="Whoa, looks like you enter an invalid stock.",
                                content_type="text",
                                complement_info="None"
                            ),
                            SingleResponse(
                                content="Try the following: search stock " + stock,
                                content_type="text",
                                complement_info="None"
                            )
                        ]
                    )
                )
            else:
                categ = get_stock_categorical_desc(stock)
                history = categ["profile"].get("company_history")#.encode('utf8', 'replace')
                trimmed_hist = history if len(history) < self.HISTORY_LIMIT else history[:self.HISTORY_LIMIT] + "... continue here: https://www.bmv.com.mx/en/issuers/profile/" + categ.get("bmv_id")#.encode('utf8', 'replace')
                self.set_response_packet(
                    ResponsePacket(
                        quick_reply_id="main_menu",
                        single_list=[
                            SingleResponse(
                                content="Company name: " + categ["company"] + ".",
                                content_type="text",
                                complement_info="None"
                            ),
                            SingleResponse(
                                content="*History*\n\n" + trimmed_hist,
                                content_type="text",
                                complement_info="None"
                            )
                        ]
                    )
                )


class CreatePortfolio(AbstractTextResponses):
    __metaclass__ = ABCMeta

    @staticmethod
    def identify_create_portfolio(text):
        text = text.lower().replace(".", "")
        return ("create portfolio" in text)

    def create_portfolio(self):
        def send_waiting_warning(sender):
            direct_text_message("Hold on! I'm generating your portfolio... ;)", str(sender))

        def extract_parameters(text):
            text = text.lower().replace(".", "").replace("create portfolio", "")
            params = {"stocks":[], "percentile":None}
            n_params = len(text.split("-")) - 1
            if not n_params:
                params["stocks"] = [s for s in text.replace(",", " ").replace("  ", " ").split(" ") if len(s)]
                params["percentile"] = 50.0
                return params
            p = text.split("-p")[-1]
            stocks = text.split("-p")[0]
            params["stocks"] = [s for s in stocks.replace(",", " ").replace("  ", " ").split(" ") if len(s)]
            try:
                params["percentile"] = float(p)
            except:
                params["percentile"] = 50.0
            return params

        def verify_stocks(stocks):
            for stock in stocks:
                if stock.upper() not in get_tickers():
                    return False
            return True

        def create_markowitz_response(resp):

            ans = """
            **Markowitz Portfolio**
            
            - *Percentile*: {p}
            - *Annual return*: {annual_return}
            - *Annual volatility*: {annual_volatility}
            """.format(
                p=str(resp["frontier-percentile"]),
                annual_return=str(resp["annual-return"]),
                annual_volatility=str(resp["annual-volatility"])
            ).replace('            ', "")
            for key in resp:
                if key in ["frontier-percentile", "annual-return", "annual-volatility", "daily-return",  "daily-volatility"]:
                    continue
                ans += "\n- *{key}*: {val}".format(key=key, val=resp[key])
            return ans

        if self.identify_create_portfolio(self.get_text()):
            parameters = extract_parameters(self.get_text())
            if not verify_stocks(parameters["stocks"]):
                self.set_response_packet(
                    ResponsePacket(
                        quick_reply_id="main_menu",
                        single_list=[
                            SingleResponse(
                                content="There's an invalid stock in your portfolio!",
                                content_type="text",
                                complement_info="None"
                            )
                        ]
                    )
                )
            else:

                symbols = [get_symbol(stock.upper()) for stock in parameters["stocks"]]
                portfolio_manager = PortfolioManager(symbols)
                send_waiting_warning(self.user_info.get_id())
                mark_resp = portfolio_manager.get_markowitz(parameters["percentile"])
                self.set_response_packet(
                    ResponsePacket(
                        quick_reply_id="main_menu",
                        single_list=[
                            SingleResponse(
                                content=create_markowitz_response(mark_resp),
                                content_type="text",
                                complement_info="None"
                            )
                        ]
                    )
                )



class AdviceStock(AbstractTextResponses):
    __metaclass__ = ABCMeta

    @staticmethod
    def identify_advice_stock(text):
        text = text.lower().replace(".", "")
        try:
            return (("advice" in text) or ("advise" in text) or ("sell or buy" in text) or ("buy or sell" in text)) and (len(text.split(" ")) < 5)
        except Exception as e:
            return False

    def advice_stock(self):
        if self.identify_advice_stock(self.get_text()):
            stock = self.get_text().split(" ")[-1].replace(";", "").replace(":", "").upper()
            if stock not in get_tickers():
                self.set_response_packet(
                    ResponsePacket(
                        quick_reply_id="main_menu",
                        single_list=[
                            SingleResponse(
                                content="Whoa, looks like you enter an invalid stock.",
                                content_type="text",
                                complement_info="None"
                            ),
                            SingleResponse(
                                content="Try the following: search stock " + stock,
                                content_type="text",
                                complement_info="None"
                            )
                        ]
                    )
                )
            else:
                symbol = get_symbol(stock)
                symbol_data = get_symbol_data(symbol)
                # probs, strategy, ratio = suggestion_strategy(symbol_data)
                try:
                    probs, strategy, ratio = suggestion_strategy(symbol_data)
                    self.set_response_packet(
                        ResponsePacket(
                            quick_reply_id="main_menu",
                            single_list=[
                                SingleResponse(
                                    content="I use an algorithm based on markov chains to decide whether to" +
                                            " buy, sell or hold a particular stock (for next-day trading). " +
                                            "For this stock ({symbol}) the algorithm generates a {ratio}".format(
                                                symbol=symbol,
                                                ratio=ratio
                                            ),
                                    content_type="text",
                                    complement_info="None"
                                ),
                                SingleResponse(
                                    content="So, my advise to you is: " + strategy + "!",
                                    content_type="text",
                                    complement_info="None"
                                ),
                                SingleResponse(
                                    content=";)",
                                    content_type="text",
                                    complement_info="None"
                                )
                            ]
                        )
                    )
                except:
                    self.set_response_packet(
                        ResponsePacket(
                            quick_reply_id="main_menu",
                            single_list=[
                                SingleResponse(
                                    content="Oh! Look that I don't have enough info to generate a trading strategy with " + symbol + ".",
                                    content_type="text",
                                    complement_info="None"
                                ),
                                SingleResponse(
                                    content="Sorry about that... You can try with another. :)",
                                    content_type="text",
                                    complement_info="None"
                                )
                            ]
                        )
                    )

class PlotStock(AbstractTextResponses):
    __metaclass__ = ABCMeta

    @staticmethod
    def identify_plot_stock(text):
        text = text.lower().replace(".", "")
        try:
            return (("plot" in text) or ("stockplot" in text)) and (len(text.split(" ")) < 3)
        except Exception as e:
            return False

    def plot_stock(self):
        if self.identify_plot_stock(self.get_text()):
            stock = self.get_text().split(" ")[-1].replace(";", "").replace(":", "").upper()
            if stock not in get_tickers():
                self.set_response_packet(
                    ResponsePacket(
                        quick_reply_id="main_menu",
                        single_list=[
                            SingleResponse(
                                content="Whoa, looks like you enter an invalid stock.",
                                content_type="text",
                                complement_info="None"
                            ),
                            SingleResponse(
                                content="Try the following: search stock " + stock,
                                content_type="text",
                                complement_info="None"
                            )
                        ]
                    )
                )
            else:
                #send_waiting_warning(self.user_info.get_id())
                symbol = get_symbol(stock)
                symbol_data = get_symbol_data(symbol)
                max_price = max([i[1] for i in symbol_data])
                self.set_response_packet(
                    ResponsePacket(
                        quick_reply_id="main_menu",
                        single_list=[
                            SingleResponse(
                                content="https://myplotlib-api.appspot.com/scatter?x=0,1,2,3,4,5&y=0,4,1,2,3,5&title=" + str(max_price),
                                content_type="image",
                                complement_info="None"
                            )
                        ]
                    )
                )


class DescribeStock(AbstractTextResponses):
    __metaclass__ = ABCMeta

    @staticmethod
    def identify_describe_stock(text):
        text = text.lower().replace(".", "")
        try:
            return (("describe" in text) or ("desc" in text)) and (len(text.split(" ")) < 4)#(text.split(" ")[-1].upper() in get_tickers())
        except Exception as e:
            return False

    def describe_stock(self):
        def send_waiting_warning(sender):
            direct_text_message("Hold on! I'm retrieving the data for you... :)", str(sender))

        def wake_up_heroku():
            try:
                r = requests.get("https://bmv-info-api.herokuapp.com/stocks/")
            except:
                r = None

        def create_categ_desc(stock_description):
            categ = stock_description["categorical"]
            resp = """**Categorical Description**
            - *Sector*: {sector}
            - *Branch*: {branch}
            - *Sub-sector*: {sub_sector}
            - *Sub-branch*: {sub_branch}
            - *Economic activity*: {economic_activity}
            - *Main Products and services*: {main_products_and_services}
            
            """.format(
                sector=categ['profile'].get('sector').encode('utf8', 'replace').lower(),
                sub_sector=categ['profile'].get('sub_sector').encode('utf8', 'replace').lower(),
                branch=categ['profile'].get('branch').encode('utf8', 'replace').lower(),
                sub_branch=categ['profile'].get('sub_branch').encode('utf8', 'replace').lower(),
                economic_activity=categ['profile'].get('economic_activity').encode('utf8', 'replace').lower(),
                main_products_and_services=categ['profile'].get('main_products_and_services').encode('utf8', 'replace').lower()
            ).replace('            ', "")

            return resp

        def create_stock_indicators_desc(stock_description):
            if "service_not_available" in stock_description["statistical"]:
                return "**Stock Indicators**\n\n <service-not-available>"
            indicators = stock_description["statistical"]["stock_indicators"]
            resp = """**Stock Indicators**
            Using information from the {quarter}.
            - *Price/Earnings Ratio*: {pe}
            - *Price/Book Value Ratio*: {pb} 
            - *Earnings Per Share Ratio*: {eps} 
            - *Book Value per Share*: {bps}
            - *Shares Outstanding*: {so}
            """.format(
                quarter=indicators["text"].split("\n")[0].lower(),
                pe=indicators.get('price_earnings_ratio'),
                pb=indicators.get('price_book_value_ratio'),
                eps=indicators.get('earnings_per_share'),
                bps=indicators.get('book_value_per_share'),
                so=indicators.get('shares_outstanding')
            ).replace('            ', "")
            return resp

        def create_stock_rates_desc(stock_description):
            if "service_not_available" in stock_description["statistical"]:
                return "**Stock Market Rates**\n\n <service-not-available>"
            market_rates = stock_description["statistical"]['stock_market_rates']
            resp = """**Stock Market Rates**
            Information of the stock performance so far (20 min. lag) for date {date}. 
            - *Price* (bid, ask) = ({bid_price}, {ask_price})
            - *Volume* (bid, ask) = ({bid_vol}, {ask_vol})
            - *Last Traded Price*: {last_trade_price}
            - *Previous Price*: {prev_price}
            - *Change*: {change}
            - *Max-Price*: {max_price}
            - *Min-Price*: {min_price}
            - *Traded Volume*: {traded_vol}
            """.format(
                date=market_rates.get("date"),
                bid_price=market_rates.get("bid_price"),
                ask_price=market_rates.get("ask_price"),
                bid_vol=market_rates.get("bid_vol"),
                ask_vol=market_rates.get("ask_vol"),
                last_trade_price=market_rates.get("last_trade_price"),
                prev_price=market_rates.get("prev_price"),
                change=market_rates.get("change"),
                max_price=market_rates.get("max_price"),
                min_price=market_rates.get("min_price"),
                traded_vol=market_rates.get("traded_vol")
            ).replace('            ', "")
            return resp

        if self.identify_describe_stock(self.get_text()):
            stock = self.get_text().split(" ")[-1].replace(";", "").replace(":", "").upper()
            if stock not in get_tickers():
                self.set_response_packet(
                    ResponsePacket(
                        quick_reply_id="main_menu",
                        single_list=[
                            SingleResponse(
                                content="Whoa, looks like you enter an invalid stock.",
                                content_type="text",
                                complement_info="None"
                            ),
                            SingleResponse(
                                content="Try the following: search stock " + stock,
                                content_type="text",
                                complement_info="None"
                            )
                        ]
                    )
                )
            else:
                send_waiting_warning(self.user_info.get_id())
                wake_up_heroku()
                stock_description = get_stock_desc(stock)
                self.set_response_packet(
                    ResponsePacket(
                        quick_reply_id="main_menu",
                        single_list=[
                            SingleResponse(
                                content="This stock belongs to the company: " + stock_description["categorical"].get("company") + ".",
                                content_type="text",
                                complement_info="None"
                            ),
                            SingleResponse(
                                content=create_categ_desc(stock_description),
                                content_type="text",
                                complement_info="None"
                            ),
                            SingleResponse(
                                content=create_stock_indicators_desc(stock_description),
                                content_type="text",
                                complement_info="None"
                            ),
                            SingleResponse(
                                content=create_stock_rates_desc(stock_description),
                                content_type="text",
                                complement_info="None"
                            )
                        ]
                    )
                )

#class StatStockDescription():


class GenericMessage(AbstractTextResponses):
    __metaclass__ = ABCMeta

    @staticmethod
    def repeat_text(first_name, text):
        try:
            out = first_name + ", there are some thing I still don't understand. Such as: '{}'.".format(text)
        except UnicodeEncodeError:
            out = "Whoa! Nice one. ;)"
        return out

    def generic(self):
        if self.get_response_packet() is None:
            sorry_msg = [
                "I'll have to excuse myself. I'm still learning to talk here! Don't push it. ;)",
                "Sorry I didn't follow. Let's talk about something else! :)"
            ]
            self.set_response_packet(
                ResponsePacket(
                    quick_reply_id="main_menu",
                    single_list=[
                        SingleResponse(
                            content=self.repeat_text(self.get_first_name(), self.get_text()),
                            content_type="text",
                            complement_info="None"
                        ),
                        SingleResponse(
                            content=random.choice(sorry_msg),
                            content_type="text",
                            complement_info="None"
                        )
                    ]
                )
            )


class TextResponses(HelloMessages, AcceptMessages, GenericMessage, PresentYourself,
                    SearchStock, DescribeStock, CompanyHistory, PlotStock, AdviceStock, CreatePortfolio):

    def __init__(self, text, user_info):
        self.user_info = user_info
        self.text = text.encode('utf8', 'replace')  #.decode('utf-8')
        self.response_packet = None

    def get_first_name(self):
        try:
            return str(self.user_info.get_first_name().decode('utf-8'))
        except Exception as e:
            return "Fellow human."

    def get_text(self):
        return str(self.text)

    def get_response_packet(self):
        return self.response_packet

    def set_response_packet(self, response_packet):
        self.response_packet = response_packet

    def generate(self):
        self.search_stock()
        self.create_portfolio()
        self.describe_stock()
        self.company_history()
        self.advice_stock()
        self.plot_stock()
        self.hello_world()
        self.name_yourself()
        self.present_yourself()
        self.accept()
        self.generic()
        return self.response_packet

