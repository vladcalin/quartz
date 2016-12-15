import datetime
from collections import namedtuple
import random
from concurrent.futures import ThreadPoolExecutor

import humanize

from tornado.web import RequestHandler
from tornado.gen import coroutine

from eventer_server import __version__
from eventer_server.models import Project

ProjectMock = namedtuple("Project", "name description owner category_count event_count last_event_humanized")


def test_get_projects():
    for i in range(30):
        yield ProjectMock(name="test.project.{}".format(i), description="Test project", owner="Vlad Calin",
                          category_count=random.randint(10, 200), event_count=random.randint(0, 100000),
                          last_event_humanized=humanize.naturaltime(
                              datetime.datetime.now() - datetime.timedelta(minutes=random.randint(0, 100))))


_executor = ThreadPoolExecutor()


class DashboardHandler(RequestHandler):
    @coroutine
    def get(self):
        projects = yield _executor.submit(Project.objects.all())
        ordered = list(sorted(projects, key=lambda x: x.event_count(hours=1)))[:5]

        event_category_count = sum([x.event_category_count for x in projects])
        event_count = sum([x.event_count() for x in projects])

        self.render("dashboard.html", version=__version__, require_morris=True, require_datatable=False,
                    project_count=len(projects),
                    projects=ordered, event_count=event_count, event_category_count=event_category_count)


class ProjectsHandler(RequestHandler):
    @coroutine
    def get(self):
        projects = yield _executor.submit(Project.objects.all())

        self.render("projects.html", version=__version__, require_morris=False, require_datatable=True,
                    projects=projects)


class EventTypesHandler(RequestHandler):
    @coroutine
    def get(self):
        self.render("event_types.html", version=__version__, require_morris=False, require_datatable=False)


class EventsHandler(RequestHandler):
    @coroutine
    def get(self):
        self.render("events.html", version=__version__, require_morris=False, require_datatable=False)


class StatusHandler(RequestHandler):
    @coroutine
    def get(self):
        self.render("status.html", version=__version__, require_morris=True, require_datatable=False)
