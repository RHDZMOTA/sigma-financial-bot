# -*- coding: utf-8 -*-
import requests
import time
import json

from settings import config
from app.mod_fb_messenger.service.QuickReplier import QuickReplier
from app.mod_fb_messenger.service.MessageManager import MessageManager
from app.mod_fb_messenger.model.MessageDatastore import IncomingMessageModel
from app.mod_fb_messenger.model import RegisterUser, MessageInfo, MessageDatastore, ResponseDatastore,\
    TextMessage, ImageMessage


def send_message(dict_resp):
    params = {"access_token": config.PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = json.dumps(dict_resp)
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params,
                      headers=headers,
                      data=data)


class EntryManager(object):

    def __init__(self, entry):
        self.entry = entry
        self.responses = []
        self.conver_infos = []
        self.message_postback_list = []
        self.delivery_list = []
        self.optin_list = []
        for message_event in entry['messaging']:
            if message_event.get('message') or message_event.get('postback'):
                self.message_postback_list.append(message_event)
            if message_event.get('delivery'):
                self.delivery_list.append(message_event)
            if message_event.get('optin'):
                self.optin_list.append(message_event)

    def send_messages(self):
        self.get_responses()
        messages = []
        for rop in self.responses:
            messages.append(rop.send_all())
            ResponseDatastore(rop).save_packet()
        return messages

    def get_responses(self):
        epoch_time = int(time.time())
        for message in self.message_postback_list:

            message_info = MessageInfo(message)

            # NOTE: This is needed in order to avoid answering multiple times the same message.
            query = IncomingMessageModel.query(
                IncomingMessageModel.unix_query > epoch_time - 25,  # TODO: refactor this.
                IncomingMessageModel.sender == int(message_info.sender),
                IncomingMessageModel.text == message_info.text
            ).fetch(limit=1)
            if len(query) and (message_info.payload is None):
                continue
            MessageDatastore(message_info).save_message()
            user_info = RegisterUser(sender=message_info.sender).get_info()
            response_packet = MessageManager(message_info, user_info).get_responses()
            rop = ResponseObjectPacket(response_packet, message_info)
            self.responses.append(rop)


class ResponseObject(object):
    def __init__(self, sender, single_response, response_packet, last):
        self.sender = sender
        self.content = single_response.content
        self.content_type = single_response.content_type
        self.complement_info = single_response.complement_info
        self.quick_reply_id = response_packet.quick_reply_id if last else ""
        self.quick_reply = QuickReplier(response_packet.quick_reply_id)

    def send(self):
        send_message(self.to_dict())

    def to_dict(self):
        message = self.get_message()
        return {
            "recipient": {
                "id": str(self.sender)
            },
            "message": message.to_dict()
        }

    def get_message(self):
        if self.content_type == "text":
            message = self.type_text()
        elif self.content_type == "image":
            message = self.type_image()
        else:
            message = None
        return message

    def type_text(self):
        return TextMessage(content=self.content, quick_reply=self.quick_reply)

    def type_image(self):
        return ImageMessage(content=self.content, quick_reply=self.quick_reply)


class ResponseObjectPacket(object):
    def __init__(self, response_packet, message_info):
        self.response_packet = response_packet
        self.message_info = message_info

    def send_all(self):
        dict_list = []
        for ro in self.list():
            ro.send()
            dict_list.append(ro.to_dict())
        return dict_list

    def list(self):
        counter = 1
        packet = []
        for single_response in self.response_packet.single_responses:
            ro = ResponseObject(
                sender=self.message_info.sender,
                single_response=single_response,
                response_packet=self.response_packet,
                last=counter == len(self.response_packet.single_responses)
            )
            packet.append(ro)
        return packet
