# -*- coding: utf-8 -*-
import requests

from settings.config import PAGE_ACCESS_TOKEN, USER_PROFILE_API


class UserInfo(object):

    def __init__(self, sender):
        self.id = sender
        self.user_url = None
        self.data = None
        self.get_data()

    def get_data(self):
        self.user_url = USER_PROFILE_API.format(user_id=self.get_id(), token=PAGE_ACCESS_TOKEN)
        user_data = requests.get(self.user_url).json()
        self.data = user_data if not 'error' in user_data else {}

    def get_id(self):
        return self.id

    def _get_x(self, x):
        return self.data.get(x)

    def get_profile_pic(self):
        return self._get_x("profile_pic")

    def get_name(self):
        if not (isinstance(self.get_last_name(), str) and isinstance(self.get_first_name(), str)):
            return " "
        if not isinstance(self.get_last_name(), str):
            return self.get_first_name()
        if not isinstance(self.get_first_name(), str):
            return self.get_last_name()
        return "{first} {last}".format(first=self.get_first_name(), last=self.get_last_name())

    def get_first_name(self):
        return self._get_x("first_name")

    def get_last_name(self):
        return self._get_x("last_name")

    def get_gender(self):
        return self._get_x("gender")

    def to_string(self):
        return "Name: {fist_name}\nLast Name: {last_name}\nGender: {gender}\nMessenger ID: {id}\nProfile Pic: {profile}".format(
            fist_name=str(self.get_first_name().encode('utf8', 'replace')),
            id=str(self.get_id().encode('utf8', 'replace')),
            last_name=str(self.get_last_name().encode('utf8', 'replace')),
            gender=str(self.get_gender().encode('utf8', 'replace')),
            profile=str(self.get_profile_pic().encode('utf8', 'replace'))
        )
