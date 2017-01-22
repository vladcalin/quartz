from tornado.gen import coroutine

from quartz.handlers.base import QuartzBaseRequestHandler


class RegisterRequestHandler(QuartzBaseRequestHandler):
    @coroutine
    def get(self):
        self.render("register.html")
