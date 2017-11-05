# -*- coding: utf-8 -*-
from util.base_model import SimpleModel


class SingleResponse(SimpleModel):
    def __init__(self, content, content_type, complement_info):
        self.content = content
        self.content_type = content_type
        self.complement_info = complement_info


class ResponsePacket(SimpleModel):
    def __init__(self, single_list, quick_reply_id):
        self.single_responses = single_list
        self.quick_reply_id = quick_reply_id


class TextMessage(object):
    def __init__(self, content, quick_reply):
        self.content = content
        self.quick_replies = quick_reply

    def to_dict(self):
        return {
            "text": self.content,
            "quick_replies": self.quick_replies.to_dict()
        }


class ImageMessage(object):
    def __init__(self, content, quick_reply):
        self.content = content
        self.quick_replies = quick_reply

    def to_dict(self):
        return {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": self.content,
                    "is_reusable": False
                }
            },
            "quick_replies": self.quick_replies.to_dict()
        }
