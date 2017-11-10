import time
from util.base_model import SerializableModel, db


class IncomingMessageModel(SerializableModel):
    created_at = db.DateTimeProperty(auto_now_add=True)
    unix_query = db.IntegerProperty(required=True)
    sender = db.IntegerProperty(required=True)
    text = db.StringProperty()
    attachments = db.StringProperty()
    payload = db.StringProperty()


class MessageInfo(object):
    def __init__(self, message_element):
        self.sender = message_element['sender'].get('id')
        self.text = message_element['message'].get('text')
        self.payload = None if not message_element['message'].get('quick_reply') \
            else message_element['message']['quick_reply']['payload']
        self.attachments = message_element['message'].get('attachments')


class MessageDatastore(object):

    def __init__(self, message_info):
        self.message_info = message_info
        self.epoch_time = int(time.time())

    def save_message(self):
        IncomingMessageModel(
            unix_query=self.epoch_time,
            sender=int(self.message_info.sender),
            text=self.message_info.text,
            attachments=str(self.message_info.attachments),
            payload=self.message_info.payload
        ).build()
