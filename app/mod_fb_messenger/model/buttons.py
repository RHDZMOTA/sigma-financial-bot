# -*- coding: utf-8 -*-
from util.base_model import SimpleModel


class UrlButton(SimpleModel):
    def __init__(self, type, title, url):
        self.type = type
        self.title = title,
        self.url = url


class PostbackButton(SimpleModel):
    def __init__(self, type, title, url):
        self.type = type
        self.title = title,
        self.url = url
