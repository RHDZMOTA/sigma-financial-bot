# -*- coding: utf-8 -*-
from app.mod_fb_messenger.service.TextResponses import TextResponses
from app.mod_fb_messenger.service.PayloadResponses import PayloadResponses
from app.mod_fb_messenger.service.AttachmentResponses import AttachmentResponses
from app.mod_fb_messenger.service.AnythingElseResponses import AnythingElseResponses


class MessageManager(object):

    def __init__(self, message_info, user_info):
        self.user_info = user_info
        self.text = message_info.text
        self.payload = message_info.payload
        self.attachments = message_info.attachments
        self.sender = message_info.sender
        self.responses = None

    def get_responses(self):
        if self.payload:
            response_packet = PayloadResponses(self.payload, self.user_info).generate()
        elif self.attachments:
            response_packet = AttachmentResponses(self.attachments, self.user_info).generate()
        elif self.text:
            response_packet = TextResponses(self.text, self.user_info).generate()
        else:
            response_packet = AnythingElseResponses(self.user_info).generate()
        return response_packet
