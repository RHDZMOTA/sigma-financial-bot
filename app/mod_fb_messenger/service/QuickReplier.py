# -*- coding: utf-8 -*-
from app.mod_fb_messenger.model import QuickReply, QuickText, AbstractQuickReplies, ABCMeta


class MainMenuButtons(AbstractQuickReplies):
    __metaclass__ = ABCMeta

    def main_menu(self):
        if (self.get_reply_type() == "main_menu") or (self.get_response() is None):
            self.set_response(
                QuickReply(
                    list_quick_objects=[
                        QuickText(title="Advises", payload="financial_advice", content_type="text"),
                        QuickText(title="Stocks", payload="show_stocks", content_type="text"),
                        QuickText(title="More options", payload="more_options", content_type="text")
                    ],
                    group="main_menu")
            )


class MoreOptsButtons(AbstractQuickReplies):
    __metaclass__ = ABCMeta

    def more_options(self):
        if self.get_reply_type() == "more_options":
            self.set_response(
                QuickReply(
                    list_quick_objects=[
                        QuickText(title="My info", payload="my_fb_info", content_type="text"),
                        QuickText(title="Heads or tails?", payload="flip_coin", content_type="text")
                    ],
                    group="more_options")
            )


class QuickReplier(MainMenuButtons, MoreOptsButtons):
    def __init__(self, quick_reply):
        self.response = None
        self.reply_type = quick_reply

    def get_response(self):
        return self.response

    def set_response(self, response):
        self.response = response

    def get_reply_type(self):
        return str(self.reply_type)

    def to_dict(self):
        self.generate_quick_reply()
        return self.response.to_dict()

    def generate_quick_reply(self):
        self.more_options()
        self.main_menu()
