# -*- coding: utf-8 -*-
from util.base_model import SerializableModel, db
from util.user_related import UserInfo


class UserModel(SerializableModel):
    user_id = db.IntegerProperty(required=True)
    user_fname = db.StringProperty()
    user_lname = db.StringProperty()
    user_gender = db.StringProperty()


class RegisterUser(object):

    def __init__(self, sender):
        self.user_info = UserInfo(sender=sender)
        self.user = None
        self.get_or_build()

    def get_or_build(self):
        users = UserModel.query(UserModel.user_id == int(self.user_info.get_id())).fetch(limit=5) #.all()
        #results = users.filter("user_id =", int(self.user_info.get_id())).fetch()
        if not len(users):
            self.user = UserModel(
                user_id=int(self.user_info.get_id()),
                user_fname=self.user_info.get_first_name(),
                user_lname=self.user_info.get_last_name(),
                user_gender=self.user_info.get_gender()
            ).build()

    def get_info(self):
        return self.user_info
