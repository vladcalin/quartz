import logging
import datetime
import uuid

from mongoengine import connect, Document, StringField, IntField, BooleanField, BinaryField, DateTimeField, \
    ReferenceField, DictField, ListField

from eventer.errors import CategoryValidationError

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

        ALL = [NUMERIC, STRING, BOOLEAN]

    class FieldConstraint:
        # universal
        REQUIRED = "required"
        DEFAULT = "default"

        # int
        MAX_VALUE = "max_val"
        MIN_VALUE = "min_val"

        # str
        MIN_LENGTH = "min_len"
        MAX_LENGTH = "max_len"
        REGEX = "regex"

    _generic_constraints = [FieldConstraint.DEFAULT, FieldConstraint.REQUIRED]

    _allowed_constraints = {
        FieldType.NUMERIC: _generic_constraints + [FieldConstraint.MIN_VALUE,
                                                   FieldConstraint.MAX_VALUE],
        FieldType.STRING: _generic_constraints + [FieldConstraint.MIN_LENGTH,
                                                  FieldConstraint.MAX_LENGTH, FieldConstraint.REGEX],
        FieldType.BOOLEAN: _generic_constraints
    }

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
    fields = ListField(required=True)

    meta = {
        "fields": [
            "#user"
        ]
    }

    @classmethod
    def field_is_valid(cls, field_dict):
        for req_field in ["name", "description", "type", "constraints"]:
            if req_field not in field_dict:
                raise ValueError("Field {} does not contain the key {}".format(field_dict, req_field))

        if not field_dict["name"]:
            raise ValueError("Field 'name' is mandatory")

        cls.check_constraints_validity(field_dict)

    @classmethod
    def check_constraints_validity(cls, field_dict):
        for constraint in field_dict["constraints"]:
            logging.error(constraint)
            if constraint not in cls._allowed_constraints[field_dict["type"]]:
                raise CategoryValidationError(
                    "Constraint {} not allowed for type {}".format(constraint, field_dict["type"]))


class Event(Document):
    category = ReferenceField(EventCategory, null=False)
    timestamp = DateTimeField(default=datetime.datetime.now)
    values = DictField()

    def validate_values(self):
        pass
