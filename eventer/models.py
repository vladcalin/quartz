import logging
import datetime
import uuid
import bcrypt

from mongoengine import connect, Document, StringField, IntField, BooleanField, BinaryField, DateTimeField, \
    ReferenceField, DictField, ListField, ValidationError, EmailField, EmbeddedDocument, EmbeddedDocumentListField, \
    UUIDField

from eventer.errors import CategoryValidationError, FieldNotFoundError, InvalidValueError
from eventer.util import generate_uuid_token
from eventer.constraints import constraint_str_length_max, constraint_str_length_min, constraint_str_regex

connect(db="eventer", host="127.0.0.1", port=27017)


class ApiToken(EmbeddedDocument):
    token = UUIDField(unique=True, default=uuid.uuid4)
    created = DateTimeField(default=datetime.datetime.now)

    def to_dict(self):
        return {
            "token": str(self.token),
            "created": str(self.created)
        }

    def __eq__(self, other):
        if not isinstance(other, ApiToken):
            return False

        return str(self.token) == str(other.token)


class User(Document):
    username = StringField(unique=True)
    first_name = StringField()
    last_name = StringField()
    email = EmailField(unique=True)
    password = BinaryField()
    active = BooleanField(default=True)
    date_joined = DateTimeField(default=datetime.datetime.now)

    api_tokens = EmbeddedDocumentListField(ApiToken)

    meta = {
        "indexes": [
            "api_tokens.token"
        ]
    }

    def generate_api_token(self):
        new_api_token = generate_uuid_token()
        self.api_tokens.append(ApiToken(token=new_api_token))
        self.save()

    def revoke_api_token(self, token):
        try:
            self.api_tokens.remove(ApiToken(token=token))
            self.save()
        except ValueError:
            raise InvalidValueError("Invalid API token parameter")

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

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_joined": str(self.date_joined),
            "api_tokens": [x.to_dict() for x in self.api_tokens]
        }


class EventFieldConstraint(EmbeddedDocument):
    """
    A constraint for a :py:class:`eventer.models.EventField` instance.
    """

    class Names:
        """
        Supported constraints names.
        """
        str_len_min = "str_len_min"
        str_len_max = "str_len_max"
        str_regex = "str_regex"

    _defined_constraints = {
        Names.str_len_min: constraint_str_length_min,
        Names.str_len_max: constraint_str_length_max,
        Names.str_regex: constraint_str_regex
    }

    type = StringField(choices=tuple(_defined_constraints.keys()))
    parameters = ListField()

    def is_valid(self, value):
        """
        Checks if the given **value** violates this constraint. If it returns True, the value is valid, if it returns
        False, the value violates this constraint.

        :param value: value to be checked
        :return:
        """
        func = self._defined_constraints.get(self.type)
        return func(value, *list(self.parameters))


class EventField(EmbeddedDocument):
    """
    Represents a field declaration of some :py:class:`eventer.models.EventCategory`.
    """

    INTEGER = 0
    """Field is a int-type value"""

    STRING = 1
    """Field is a str-type value"""

    BOOLEAN = 2
    """Field is a boolean-type value (True or False)"""

    name = StringField()
    description = StringField()
    type = IntField(choices=(INTEGER, STRING, BOOLEAN))
    constraints = EmbeddedDocumentListField(EventFieldConstraint)
    required = BooleanField(default=False)
    default = StringField(default="")


class EventCategory(Document):
    """
    Represents the definition of an event category. In this object will
    be defined the following:

    - the metadata of the category (name, description, owner)
    - the field declaration: :py:class:`eventer.models.EventField`
    objects that define how the fields look-like (what name do they have,
    what they represent, expected value type, required or not, etc).
    See :py:class:`eventer.models.EventField` documentation for more info.
    - the constraints for each field (see :py:class:`eventer.models.EventFieldConstraint`
    for more information).
    """

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
    """
    Specific event that will be inserted into the database.

    .. important::

        Each event field value must respect all the constraints
        defined in the corresponding field from the event category
        declaration.

    """
    category = ReferenceField(EventCategory, null=False)
    timestamp = DateTimeField(default=datetime.datetime.now)
    values = DictField()
