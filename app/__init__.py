from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from google.appengine.ext import db

app = Flask(__name__)
app.config.from_object('app_config')
#db = SQLAlchemy(app)

# FB-Messenger-Webhook
from app.mod_fb_messenger.controller import mod_fb_messenger as fb_messenger
app.register_blueprint(fb_messenger)
