import logging
import datetime
import uuid

from mongoengine import connect, Document, StringField, IntField, BooleanField, BinaryField, DateTimeField, \
    ReferenceField, DictField

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

    meta = {
        "indexes": [
            "#session_token"
        ]
    }

    @staticmethod
    def generate_session_token():
        return str(uuid.uuid4())

    def renew_session(self):
        self.session_token = self.generate_session_token()
        self.save()

    def invalidate_session(self):
        self.session_token = None
        self.save()


class EventCategory(Document):
    class FieldType:
        NUMERIC = "int"
        STRING = "str"
        BOOLEAN = "bool"
        DATETIME = "datetime"

        ALL = [NUMERIC, STRING, BOOLEAN, DATETIME]

    class FieldConstraint:
        # universal
        REQUIRED = "req"
        DEFAULT = "default"

        # int
        MAX_VALUE = "max_val"
        MIN_VALUE = "min_val"

        # str
        MIN_LENGTH = "min_len"
        MAX_LENGTH = "max_len"
        REGEX = "regex"

    name = StringField(unique=True)
    description = StringField()
    user = ReferenceField(User)

    """
        Field specification will be kept in the following form:
            {
                name: ...,
                description: ...,
                type: ...,
                constraints: ...
            }
    """
    fields = DictField(required=True)

    meta = {
        "fields": [
            "#user"
        ]
    }

    def field_is_valid(self, field_dict):
        for req_field in ["name", "description", "type", "constraints"]:
            if req_field not in field_dict:
                raise ValueError("Field {} does not contain the key {}".format(field_dict, req_field))

        if not field_dict["name"]:
            raise ValueError("Field 'name' is mandatory")




class Event(Document):
    category = ReferenceField(EventCategory, null=False)
    timestamp = DateTimeField(default=datetime.datetime.now)
    values = DictField()

    def validate_values(self):
        pass
