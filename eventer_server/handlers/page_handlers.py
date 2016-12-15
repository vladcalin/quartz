from tornado.web import RequestHandler
from tornado.gen import coroutine

from eventer_server import __version__


class DashboardHandler(RequestHandler):
    @coroutine
    def get(self):
        self.render("dashboard.html", version=__version__, require_morris=True, require_datatable=False)


class ProjectsHandler(RequestHandler):
    @coroutine
    def get(self):
        self.render("projects.html", version=__version__, require_morris=False, require_datatable=True)


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
