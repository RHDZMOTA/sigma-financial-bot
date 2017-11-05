# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class AbstractQuickReplies:
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_response(self, response_packet):
        pass

    @abstractmethod
    def get_response(self):
        pass

    @abstractmethod
    def get_reply_type(self):
        pass
