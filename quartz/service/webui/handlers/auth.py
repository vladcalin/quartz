from tornado.gen import coroutine

from quartz.service.webui.handlers import QuartzBaseRequestHandler


class RegisterRequestHandler(QuartzBaseRequestHandler):
    @coroutine
    def get(self):
        self.render("register.html")
