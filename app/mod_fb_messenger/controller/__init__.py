import settings.config as config
import json

from flask import Blueprint, request, flash, g, session, redirect, url_for, jsonify
from app import app

from app.mod_fb_messenger.service import FacebookWebHook, EntryManager


mod_fb_messenger = Blueprint('fb-messenger', __name__, url_prefix='/fb-messenger')


@mod_fb_messenger.route('/sigma-bot', methods=['GET'])
def identify_fb_messenger():
    return FacebookWebHook(
        hub_mode=request.args.get("hub.mode"),
        hub_verify_token=request.args.get("hub.verify_token"),
        hub_challenge=request.args.get("hub.challenge")).response()


@mod_fb_messenger.route('/sigma-bot', methods=['POST'])
def post_web_hook():
    data = request.get_json()
    messages_list = []
    if data.get("object") == "page":
        for entry in data["entry"]:
            messages = EntryManager(entry).send_messages()
            messages_list.append(messages)
    return json.dumps({"message_list": messages_list}), 200
