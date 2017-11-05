# -*- coding: utf-8 -*-
from app.mod_fb_messenger.model import ResponsePacket, SingleResponse
from google.appengine.api import urlfetch


urlfetch.set_default_fetch_deadline(60)


class AttachmentResponses(object):

    def __init__(self, attachment_dict, user_info):
        self.user_info = user_info
        self.attachment_dict = attachment_dict
        self.response_packet = None

    def generate(self):
        self.respond_image_url()
        self.generic()
        return self.response_packet

    def respond_image_url(self):

        if "image" in str(self.attachment_dict[0]['type']):
            image_url = str(self.attachment_dict[0]['payload'].get("url"))

            self.response_packet = ResponsePacket(
                quick_reply_id="main_menu",
                single_list=[
                    SingleResponse(
                        content="Thanks for your image. You can have it back here: " + image_url,
                        content_type="text",
                        complement_info="None"
                    )
                ]
            )

    def generic(self):
        if self.response_packet is None:
            self.response_packet = ResponsePacket(
                quick_reply_id="main_menu",
                single_list=[
                    SingleResponse(
                        content="Nice " + str(self.attachment_dict[0]['type']),
                        content_type="text",
                        complement_info="None"
                    )
                ]
            )
