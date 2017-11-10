# -*- coding: utf-8 -*-
from util.base_model import SerializableModel, db


class ResponseModel(SerializableModel):
    created_at = db.DateTimeProperty(auto_now_add=True)
    sender = db.IntegerProperty(required=True)
    text = db.StringProperty()
    group = db.StringProperty()
    attachment_url = db.StringProperty()
    reply_quick_id = db.StringProperty()


class ResponseDatastore(object):

    def __init__(self, rop):
        self.rop = rop
        self.datastore_response = []
        self.unicode_error = False

    def save_packet(self):
        for ro in self.rop.list():
            self.datastore_response.append(self.save_response_object(ro))

    def save_response_object(self, ro):
        response_dict = ro.to_dict()
        ro.quick_reply.generate_quick_reply()
        group = ro.quick_reply.get_response().get_group()
        try:
            msn = response_dict["message"].get("text").encode('utf8', 'replace')
        except:
            msn = "<empty or error>"  # TODO: fix this (UnicodeError)
        ResponseModel(
            sender=int(ro.sender),
            text=msn, #msn.encode('utf8', 'replace') if msn else "-".encode('utf8', 'replace'),
            attachment_url=str(response_dict["message"]["attachment"]["payload"].get("url"))\
                if response_dict["message"].get("attachment")\
                else None,
            reply_quick_id=group
        ).build()
        #try:
        #    ResponseModel(
        #        sender=int(ro.sender),
        #        text=str(response_dict["message"].get("text")),
        #        attachment_url=str(response_dict["message"]["attachment"]["payload"].get("url"))\
        #            if response_dict["message"].get("attachment")\
        #            else None,
        #        reply_quick_id=group
        #    ).build()
        #except UnicodeEncodeError as e:
        #    self.unicode_error = True