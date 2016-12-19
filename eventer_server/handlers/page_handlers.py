import datetime
from collections import namedtuple
import random
from concurrent.futures import ThreadPoolExecutor
import logging

import humanize
from mongoengine import DoesNotExist
from tornado.web import RequestHandler, HTTPError
from tornado.gen import coroutine

from eventer_server import __version__
from eventer_server.models import Project, EventCategory, FieldSpecs, Event

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
        event_count = Event.objects.count()

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


class CreateProjectHandler(RequestHandler):
    @coroutine
    def get(self):
        self.render("create_project.html", version=__version__, require_morris=False, require_datatable=False)


class ViewProjectHandler(RequestHandler):
    @coroutine
    def get(self, proj_id, *args, **kwargs):
        try:
            project = yield _executor.submit(Project.objects.get, id=proj_id)
            categories = yield _executor.submit(EventCategory.objects, project=proj_id)
        except DoesNotExist:
            raise HTTPError(404)
        self.render("project_view.html", version=__version__, require_morris=False, require_datatable=False,
                    project=project, categories=categories)


class EditProjectHandler(RequestHandler):
    @coroutine
    def get(self, proj_id, *args, **kwargs):
        try:
            project = yield _executor.submit(Project.objects.get, id=proj_id)
        except DoesNotExist:
            raise HTTPError(404)
        self.render("project_edit.html", version=__version__, require_morris=False, require_datatable=False,
                    project=project)


class CreateEventCategoryHandler(RequestHandler):
    @coroutine
    def get(self, proj_id, *args, **kwargs):
        try:
            project = yield _executor.submit(Project.objects.get, id=proj_id)
        except DoesNotExist:
            raise HTTPError(404)
        self.render("create_category.html", version=__version__, require_morris=False, require_datatable=False,
                    project=project)


class ViewEventCategory(RequestHandler):
    @coroutine
    def get(self, proj_id, event_category_id):
        try:
            project = yield _executor.submit(Project.objects.get, id=proj_id)
            event_category = yield _executor.submit(EventCategory.objects.get, id=event_category_id)

            total_events = yield _executor.submit(Event.objects.count)
            last_submitted_event = yield _executor.submit(Event.objects.only('timestamp', 'source').order_by("-timestamp").first)
        except DoesNotExist:
            raise HTTPError(404)
        self.render("category_view.html", version=__version__, require_morris=False, require_datatable=False,
                    project=project, event_category=event_category, event_count=total_events,
                    last_submit_time=humanize.naturaltime(last_submitted_event.timestamp),
                    last_submit_source=last_submitted_event.source)
