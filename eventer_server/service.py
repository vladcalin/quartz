import os
import logging
import argparse
import datetime

from tornado.web import RequestHandler
from tornado.gen import coroutine
import click

from pymicroservice.core.microservice import PyMicroService
from pymicroservice.core.decorators import public_method, private_api_method

from eventer_server.handlers.page_handlers import DashboardHandler, ProjectsHandler, EventTypesHandler, EventsHandler, \
    StatusHandler, CreateProjectHandler, ViewProjectHandler, EditProjectHandler, CreateEventCategoryHandler, \
    ViewEventCategory
from eventer_server.lib.query import QueryParser
from eventer_server.models import Project, FieldSpecs, EventCategory, Event, set_db_parameters


class EventerService(PyMicroService):
    name = "eventer_server"
    host = "127.0.0.1"
    port = 8000

    api_token_header = "X-Api-Token"
    max_parallel_blocking_tasks = os.cpu_count()

    extra_handlers = [
        ("/projects/view/([a-f0-9]+)", ViewProjectHandler),
        ("/projects/view/([a-f0-9]+)/edit", EditProjectHandler),
        ("/projects/view/([a-f0-9]+)/create_category", CreateEventCategoryHandler),
        ("/projects/view/([a-f0-9]+)/categories/([a-f0-9]+)", ViewEventCategory),
        ("/dashboard", DashboardHandler),
        ("/projects", ProjectsHandler),
        ("/event_types", EventTypesHandler),
        ("/events", EventsHandler),
        ("/status", StatusHandler),
        ("/projects/create", CreateProjectHandler),
    ]

    root_directory = os.path.dirname(os.path.abspath(__file__))
    # create your templates
    template_dir = os.path.join(root_directory, "html", "templates")

    # setup your static files
    static_dirs = [
        (r"/static", os.path.join(root_directory, "html", "static")),
    ]

    # service registries
    service_registry_urls = []
    service_registry_ping_interval = 30

    def __init__(self, host, port, registry):
        super(EventerService, self).__init__()
        self.host = host
        self.port = port
        if registry:
            self.service_registry_urls = [registry]


    @public_method
    def create_project(self, name, description, owner):
        if not name or not description or not owner:
            raise ValueError("Bad parameters submitted")
        project = Project(name=name, description=description, owner=owner)
        project.save()
        return str(project.id)

    @public_method
    def update_project(self, project_id, name=None, description=None, owner=None):
        project = Project.objects.get(id=project_id)
        if name:
            project.name = name
        if description:
            project.description = description
        if owner:
            project.owner = owner
        project.save()
        return True

    @public_method
    def delete_project(self, project_id):
        project = Project.objects.get(id=project_id)
        project.delete()
        return True

    @public_method
    def create_category(self, name, description, project_id, fields):
        field_specs = [FieldSpecs(**fieldspec) for fieldspec in fields]

        if len(set([f["name"] for f in field_specs])) != len(field_specs):
            raise ValueError("Duplicate value name")

        event_category = EventCategory(name=name, description=description, project=project_id, fields=field_specs)
        event_category.save()
        return str(event_category.id)

    @public_method
    def submit_event(self, source, category, values):
        event = Event()
        event.source = source
        event.category = category
        event.set_values(**values)

        event.save()
        return str(event.id)

    @public_method
    def query_events(self, query):
        parse_result = QueryParser().parse_query(query)
        events = Event.filter_by_query(parse_result)
        return [{
                    "timestamp": event.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "values": event.values,
                    "source": event.source
                } for event in events]

    # Implement your token validation logic
    def api_token_is_valid(self, api_token):
        return True


@click.command("run")
@click.option("--host", default="0.0.0.0", help="address to bind to")
@click.option("--port", default=8080, help="port to bind to", type=int)
@click.option("--registry", help="service registry to be used")
@click.option("--db", default="mongo://localhost:27017/eventer", help="mongodb server to be used. Uses the 'eventer' database")
def main(host, port, registry, db):
    set_db_parameters(db)
    service = EventerService(host, port, registry)
    service.start()

