import datetime
import ast
import json

import humanize
from mongoengine import connect, Document, EmbeddedDocument, ReferenceField, StringField, BooleanField, DateTimeField, \
    EmbeddedDocumentListField, BinaryField, DictField, Q

from eventer_server.lib.util import str_interval_to_datetime

connect("eventer")


class Project(Document):
    name = StringField(unique=True, required=True)
    description = StringField(default="")
    owner = StringField(required=True)

    created = DateTimeField(default=datetime.datetime.now())

    def event_count(self, hours=None):
        categories = EventCategory.objects(project=self).all()
        if hours is None:
            return sum([Event.objects(category=categ).count() for categ in categories])
        else:
            target_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
            return sum(
                [Event.objects(category=categ).filter(Q(timestamp__gte=target_time)).count() for categ in categories])

    @property
    def event_category_count(self):
        return EventCategory.objects(project=self).count()

    def last_event_humanized(self):
        return "No events"


class FieldSpecs(EmbeddedDocument):
    name = StringField()
    description = StringField(default="")
    required = BooleanField(default=False)
    default = StringField(default="null")
    type = StringField(choices=("int", "str", "bool"))


class EventCategory(Document):
    name = StringField(unique=True, required=True)
    description = StringField(default="")
    project = ReferenceField(Project)

    fields = EmbeddedDocumentListField(FieldSpecs)


class Event(Document):
    category = ReferenceField(EventCategory)
    timestamp = DateTimeField(default=datetime.datetime.now)
    source = StringField(required=False)
    values = DictField()

    def set_values(self, **kwargs):
        values_dict = {}
        if isinstance(self.category, str):
            self.category = EventCategory.objects.get(id=self.category)
        fieldspecs = self.category.fields
        fieldspecs = {spec.name: spec for spec in fieldspecs}
        for k, v in kwargs.items():
            if k not in fieldspecs:
                raise ValueError("Unknown event field: {}".format(k))

            values_dict[k] = v

        for registered_field in fieldspecs:
            if registered_field not in values_dict.keys():
                if fieldspecs[registered_field].required:
                    raise ValueError("Requiered field not set: {}".format(registered_field))
                else:
                    values_dict[registered_field] = json.loads(fieldspecs[registered_field].default)

        for valuename, value in values_dict.items():
            if not self.type_matches(value, fieldspecs[valuename].type):
                raise ValueError("Type mismatch: {}".format(valuename))
        self.values = values_dict

    def type_matches(self, value, type):
        if type not in ("int", "str", "bool"):
            raise ValueError("Invalid type name")
        type_class = eval(type)
        return isinstance(value, type_class)

    @classmethod
    def filter_by_query(cls, query_parse_result):
        """
        Filters queries based on the query parse result

        :param parse_result:
        :return:
        """
        query_params = {}
        for key, operator, value in query_parse_result.filters:
            if key == "__timestamp__":
                query_params["__timestamp__"] = str_interval_to_datetime(value)
                continue
            current_key = key
            if operator == "=":
                pass
            elif operator == ">":
                current_key += "__gt"
            elif operator == ">=":
                current_key += "__gte"
            elif operator == "<":
                current_key += "__lt"
            elif operator == "<=":
                current_key += "__lte"
            else:
                raise ValueError("Invalid operator: {}".format(operator))

            try:
                query_params[current_key] = json.loads(value)
            except Exception as e:
                query_params[current_key] = value

        print(query_params)
        category = EventCategory.objects.get(name=query_parse_result.category)

        target_datetime =query_params["__timestamp__"]
        del query_params["__timestamp__"]
        events = cls.objects(Q(category=category) & Q(timestamp__gte=target_datetime) & Q(**query_params)).all()
        return events


if __name__ == '__main__':
    Project(name="test.6", description="Just a test project", owner="rpg").save()
    Project(name="test.7", description="Just a test project", owner="rpg").save()
    Project(name="test.8", description="Just a test project", owner="rpg").save()
    Project(name="test.9", description="Just a test project", owner="rpg").save()
    Project(name="test.10", description="Just a test project", owner="rpg").save()
