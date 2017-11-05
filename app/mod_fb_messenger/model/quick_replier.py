# -*- coding: utf-8 -*-
from util.base_model import SimpleModel


class QuickText(SimpleModel):
    def __init__(self, content_type, title, payload):
        self.content_type = content_type
        self.title = title
        self.payload = payload


class QuickReply(object):

    def __init__(self, list_quick_objects, group):
        self.list = list_quick_objects
        self.to_dict_list = []
        self.group = group

    def get_group(self):
        return self.group

    def to_dict(self):
        to_dict_list = []
        for element in self.list:
            to_dict_list.append(element.to_dict())
        self.to_dict_list = to_dict_list
        return to_dict_list