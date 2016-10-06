import logging
import datetime
import uuid

from mongoengine import connect, Document, StringField, IntField, BooleanField, BinaryField, DateTimeField

connect(db="eventer", host="127.0.0.1", port=27017)


class User(Document):
    username = StringField(unique=True)
    first_name = StringField()
    last_name = StringField()
    email = StringField(unique=True)
    password = BinaryField()
    active = BooleanField(default=True)
    date_joined = DateTimeField(default=datetime.datetime.now)

    session_token = StringField()

    @staticmethod
    def generate_session_token():
        return str(uuid.uuid4())
