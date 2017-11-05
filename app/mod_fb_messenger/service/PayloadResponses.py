# -*- coding: utf-8 -*-

import random

from app.mod_fb_messenger.model import ResponsePacket, SingleResponse, AbstractPayloadResponses, ABCMeta


class MyInformation(AbstractPayloadResponses):
    __metaclass__ = ABCMeta

    def my_info(self):
        if self.get_payload() == "my_fb_info":
            user_info = """Name: {}\n"""
            self.set_response_packet(
                ResponsePacket(
                    quick_reply_id="main_menu",
                    single_list=[
                        SingleResponse(
                            content="This is all I know about you. :o",
                            content_type="text",
                            complement_info="None"
                        ),
                        SingleResponse(
                            content=self.get_user_info(),
                            content_type="text",
                            complement_info="None"
                        )
                    ]
                )
            )


class GenericResponse(AbstractPayloadResponses):
    __metaclass__ = ABCMeta

    def generic(self):
        if not self.get_response_packet():
            self.set_response_packet(
                ResponsePacket(
                    quick_reply_id="main_menu",
                    single_list=[
                        SingleResponse(
                            content="Oh jeez, unknown payload. Please contact a developer!",
                            content_type="text",
                            complement_info="None"
                        )
                    ]
                )
            )


class MoreOptions(AbstractPayloadResponses):
    __metaclass__ = ABCMeta

    def all_more_options(self):
        self.more_options()
        self.driving_advice()
        self.flip_coin()

    def more_options(self):
        if self.get_payload() == "more_options":
            content_resp = [
                "There you go :)",
                "Got it, chief. :)",
                "Alright! ;)"
            ]
            self.set_response_packet(
                ResponsePacket(
                    quick_reply_id="more_options",
                    single_list=[
                        SingleResponse(
                            content=random.choice(content_resp),
                            content_type="text",
                            complement_info="None"
                        )
                    ]
                )
            )

    def driving_advice(self):
        if self.get_payload() == "financial_advice":
            content_resp = [
                "Remember to diversify your investments! ;)",
                "Checkout blockchain and crypto-currencies. :O",
                "Don't trust technical analysis by itself.",
                "AI is your friend. Don't fear. :)"
            ]
            self.set_response_packet(
                ResponsePacket(
                    quick_reply_id="main_menu",
                    single_list=[
                        SingleResponse(
                            content=random.choice(content_resp),
                            content_type="text",
                            complement_info="None"
                        )
                    ]
                )
            )

    def flip_coin(self):
        if self.get_payload() == "flip_coin":
            content_resp = ["Heads!", "Tail!"]
            funny_recommendation = [
                "You can now go and gamble with binary options!",
                "Use this information wisely. ;)",
                "What else? :)",
                "Now go, my son, and do make that money rain!",
                "Hope you will not use this info for your investment strategies. ;)"
            ]
            self.set_response_packet(
                ResponsePacket(
                    quick_reply_id="main_menu",
                    single_list=[
                        SingleResponse(
                            content=random.choice(content_resp),
                            content_type="text",
                            complement_info="None"
                        ),
                        SingleResponse(
                            content=random.choice(funny_recommendation),
                            content_type="text",
                            complement_info="None"
                        )
                    ]
                )
            )


class PayloadResponses(MyInformation, MoreOptions, GenericResponse):

    def __init__(self, payload, user_info):
        self.user_info = user_info
        self.payload = payload
        self.response_packet = None

    def get_user_info(self):
        return str(self.user_info.to_string())

    def get_payload(self):
        return str(self.payload)

    def get_response_packet(self):
        return self.response_packet

    def set_response_packet(self, response_packet):
        self.response_packet = response_packet

    def get_first_name(self):
        try:
            return str(self.user_info.get_first_name().decode('utf-8'))
        except Exception as e:
            return "Human fellow"

    def generate(self):
        self.my_info()
        self.all_more_options()
        # add more
        self.generic()
        return self.response_packet
