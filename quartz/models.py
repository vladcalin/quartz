import urllib.parse
import datetime
import ast
import json
import uuid

import humanize

from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection, columns
from cassandra.cqlengine.models import Model

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
    # connection.setup(cluster_ips, default_keyspace="quartz")
    # sync_table(Project)
    pass



if __name__ == '__main__':
    pass
