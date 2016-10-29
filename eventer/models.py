import logging
import datetime
import uuid
import bcrypt

from mongoengine import connect, Document, StringField, IntField, BooleanField, BinaryField, DateTimeField, \
    ReferenceField, DictField, ListField, ValidationError, EmailField, EmbeddedDocument, EmbeddedDocumentListField

from eventer.errors import CategoryValidationError, FieldNotFoundError
from eventer.util import generate_uuid_token
from eventer.constraints import constraint_str_length_max, constraint_str_length_min, constraint_str_regex

connect(db="eventer", host="127.0.0.1", port=27017)


class User(Document):
    username = StringField(unique=True)
    first_name = StringField()
    last_name = StringField()
    email = EmailField(unique=True)
    password = BinaryField()
    active = BooleanField(default=True)
    date_joined = DateTimeField(default=datetime.datetime.now)

    session_token = StringField()
    api_token = StringField(unique=True, default=generate_uuid_token)

    meta = {
        "indexes": [
            "#session_token"
        ]
    }

    def renew_session(self):
        self.session_token = generate_uuid_token()
        self.save()

    def invalidate_session(self):
        self.session_token = None
        self.save()

    def count_categories(self):
        return EventCategory.objects.filter(user=self).count()

    def count_events(self):
        categories = EventCategory.objects.filter(user=self)
        return sum([Event.objects.filter(category=cat.id).count() for cat in categories])

    def set_password(self, password):
        if isinstance(password, str):
            password = password.encode()
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())

    def verify_password(self, password):
        if isinstance(password, str):
            password = password.encode()
        return bcrypt.checkpw(password, self.password)


class EventFieldConstraint(EmbeddedDocument):
    class Names:
        str_len_min = "str_len_min"
        str_len_max = "str_len_max"
        str_regex = "str_regex"

    _supported = {
        Names.str_len_min: constraint_str_length_min,
        Names.str_len_max: constraint_str_length_max,
        Names.str_regex: constraint_str_regex
    }

    type = StringField(choices=tuple(_supported.keys()))
    parameters = ListField()

    def check(self, value):
        func = self._supported.get(self.type)
        return func(value, *list(self.parameters))


class EventField(EmbeddedDocument):
    INTEGER = 0
    STRING = 1
    BOOLEAN = 2

    name = StringField()
    description = StringField()
    type = IntField(choices=(INTEGER, STRING, BOOLEAN))
    constraints = EmbeddedDocumentListField(EventFieldConstraint)


class EventCategory(Document):
    name = StringField(unique=True)
    description = StringField()
    user = ReferenceField(User)

    fields = EmbeddedDocumentListField(EventField)

    meta = {
        "fields": [
            "#user"
        ]
    }


class Event(Document):
    category = ReferenceField(EventCategory, null=False)
    timestamp = DateTimeField(default=datetime.datetime.now)
    values = DictField()
