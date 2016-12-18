import datetime

import humanize
from mongoengine import connect, Document, EmbeddedDocument, ReferenceField, StringField, BooleanField, DateTimeField, \
    EmbeddedDocumentListField, BinaryField

connect("eventer")


class Project(Document):
    name = StringField(unique=True, required=True)
    description = StringField(default="")
    owner = StringField(required=True)

    created = DateTimeField(default=datetime.datetime.now())

    def event_count(self, hours=None):
        return 0

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


if __name__ == '__main__':
    Project(name="test.6", description="Just a test project", owner="rpg").save()
    Project(name="test.7", description="Just a test project", owner="rpg").save()
    Project(name="test.8", description="Just a test project", owner="rpg").save()
    Project(name="test.9", description="Just a test project", owner="rpg").save()
    Project(name="test.10", description="Just a test project", owner="rpg").save()
