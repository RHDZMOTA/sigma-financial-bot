# -*- coding: utf-8 -*-
import random

from app.mod_fb_messenger.model import ResponsePacket, SingleResponse
from util.string_operations import replace
from abc import ABCMeta, abstractmethod
from data.stocks import get_tickers

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
        return "seach stock " in text.lower()

    def search_stock(self):
        def get_top(xs, n=10):
            xs = sorted(xs, reverse=True)
            return xs if len(xs) < n else [] if n == 0 else [xs[0]] + get_top(xs[1:], n - 1)
        if self.search_stock_invoked(self.get_text()):
            stock = self.get_text().split(" ")[-1].replace(";", "").replace(":", "").upper()
            stocks = get_tickers()
            stocks_score = [0]*len(stocks)
            for word in stock:
                stocks_score = [score + val for score, val in zip(stocks_score, [word in s for s in stocks])]
            stocks_score = [score * (float(len(stock)) / float(len(s))
                                     if len(s) > len(stock)
                                     else float(len(s)) / float(len(stock)))
                            for score, s in zip(stocks_score, stocks)]
            probable_scores = get_top(stocks_score)
            probable_stocks = [s for s, score in zip(stocks, stocks_score) if score in probable_scores]
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


class TextResponses(HelloMessages, AcceptMessages, GenericMessage, PresentYourself, SearchStock):

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
        self.hello_world()
        self.name_yourself()
        self.present_yourself()
        self.accept()
        self.generic()
        return self.response_packet

