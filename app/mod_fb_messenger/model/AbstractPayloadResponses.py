# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class AbstractPayloadResponses:
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_response_packet(self, response_packet):
        pass

    @abstractmethod
    def get_response_packet(self):
        pass

    @abstractmethod
    def get_payload(self):
        pass

    @abstractmethod
    def get_first_name(self):
        pass

    @abstractmethod
    def get_user_info(self):
        pass
