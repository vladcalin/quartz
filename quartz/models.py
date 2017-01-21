import urllib.parse
import datetime
import ast
import json
import uuid

import humanize
from mongoengine import connect, Document, EmbeddedDocument, ReferenceField, StringField, BooleanField, DateTimeField, \
    EmbeddedDocumentListField, BinaryField, DictField, Q, IntField, FloatField, CASCADE

from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection, columns
from cassandra.cqlengine.models import Model

from quartz.lib.util import str_interval_to_datetime


"""
Data models

Project {
    id: uuid [pk]
    name: text
    description: text
    owner: text
    created: datetime
    categories: list<uuid>
    tags: list<text>
}

Category {
    id: uuid [pk]
    name: text
    description: text
    created: datetime
    fields: dict<str, str>
        name: definition (definition = type,required,default # ex: "int,0,0" - integer not required, default 0)
}

Event {
    id: uuid [pk]
    category: uuid [indexed]
    timestamp: datetime [indexed]
    values: dict<str, str>
        name: json(value)
}

"""


def set_db_parameters(cluster_ips):
    connection.setup(cluster_ips, default_keyspace="quartz")
    sync_table(Project)


class Project(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text(required=True)
    description = columns.Text(default="")
    owner = columns.Text(default="Unknown")
    tags = columns.List(columns.Text)

    created = columns.DateTime(default=datetime.datetime.now)

    categories = columns.List(columns.UUID)

    def event_count(self, hours=None):
        categories = self.categories
        if hours is None:
            return sum([Event.objects(category=categ).count() for categ in categories])
        else:
            target_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
            return sum(
                [Event.objects(category=categ).filter(Q(timestamp__gte=target_time)).count() for categ in categories])

    @property
    def event_category_count(self):
        return len(list(self.categories))

    def last_event_humanized(self):
        return "No events"


class Category(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text(required=True)
    description = columns.Text(default="")
    created = columns.DateTime(default=datetime.datetime.now)
    fields = columns.Map(columns.Text, columns.Text)


class Event(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    category = columns.UUID(required=True, index=True, partition_key=True)
    values = columns.Map(columns.Text, columns.Blob)
    timestamp = columns.DateTime(default=datetime.datetime.now)


class QueryHistory(Document):
    pass


if __name__ == '__main__':
    pass
