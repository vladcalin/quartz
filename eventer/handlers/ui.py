import tornado.gen

from eventer.handlers.base import HttpPageHandler, AuthenticationRequiredHandler
from eventer.models import EventCategory, User


class IndexHandler(HttpPageHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render("index.html", **self.get_default_context())


class DocumentationHandler(HttpPageHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render("doc.html", **self.get_default_context())


class LoginHandler(HttpPageHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render("login.html", **self.get_default_context())


class RegisterHandler(HttpPageHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render("register.html", **self.get_default_context())


class EventsHandler(AuthenticationRequiredHandler):
    @tornado.gen.coroutine
    def get(self):
        events = EventCategory.objects.filter(user=self.current_user)
        self.render("events.html", events=events, **self.get_default_context())


class CreateEventCategoryHandler(AuthenticationRequiredHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render("create_event_category.html", **self.get_default_context())
