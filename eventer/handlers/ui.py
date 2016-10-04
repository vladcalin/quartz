import tornado.gen

from eventer.handlers.base import HttpPageHandler


class IndexHandler(HttpPageHandler):

    @tornado.gen.coroutine
    def get(self):
        self.render("index.html", **self.get_default_context())
