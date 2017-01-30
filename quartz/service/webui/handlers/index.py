from tornado.gen import coroutine

from quartz.service.webui.handlers import QuartzBaseRequestHandler


class IndexRequestHandler(QuartzBaseRequestHandler):
    @coroutine
    def get(self):
        self.render("index.html")
