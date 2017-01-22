from tornado.web import RequestHandler
from tornado.gen import coroutine

from quartz.handlers.base import QuartzBaseRequestHandler


class IndexRequestHandler(QuartzBaseRequestHandler):
    @coroutine
    def get(self):
        self.render("index.html")
