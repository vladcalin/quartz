import os
import logging

from tornado.web import RequestHandler
from tornado.gen import coroutine

from pymicroservice.core.microservice import PyMicroService
from pymicroservice.core.decorators import public_method, private_api_method

from eventer_server.handlers.page_handlers import DashboardHandler, ProjectsHandler, EventTypesHandler, EventsHandler, \
    StatusHandler, CreateProjectHandler, ViewProjectHandler
from eventer_server.models import Project


class EventerService(PyMicroService):
    name = "eventer_server"
    host = "127.0.0.1"
    port = 8000

    api_token_header = "X-Api-Token"
    max_parallel_blocking_tasks = os.cpu_count()

    extra_handlers = [
        ("/projects/view/([a-f0-9]+)", ViewProjectHandler),
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

    def __init__(self):
        self._values = {}
        super(EventerService, self).__init__()

    @public_method
    def create_project(self, name, description, owner):
        if not name or not description or not owner:
            raise ValueError("Bad parameters submitted")
        project = Project(name=name, description=description, owner=owner)
        project.save()
        return str(project.id)

    # Implement your token validation logic
    def api_token_is_valid(self, api_token):
        return True


if __name__ == '__main__':
    service = EventerService()
    service.start()
