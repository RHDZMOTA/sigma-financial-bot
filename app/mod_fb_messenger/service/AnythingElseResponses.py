# -*- coding: utf-8 -*-
from app.mod_fb_messenger.model import ResponsePacket, SingleResponse


class AnythingElseResponses(object):

    def __init__(self, user_info, something=None):
        self.user_info = user_info
        self.something = something
        self.response_packet = None

    def generate(self):
        self.random_answer()
        return self.response_packet

    def random_answer(self):
        self.response_packet = ResponsePacket(
            quick_reply_id="main_menu",
            single_list=[
                SingleResponse(
                    content="Wow! Object not recognizable.",
                    content_type="text",
                    complement_info="None"
                ),
                SingleResponse(
                    content="Merci beaucoup. ;)",
                    content_type="text",
                    complement_info="None"
                )
            ]
        )