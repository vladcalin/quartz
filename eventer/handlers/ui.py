import tornado.gen

from eventer.handlers.base import HttpPageHandler


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
