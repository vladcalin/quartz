from tornado.web import RequestHandler
from tornado.gen import coroutine

from quartz import __version__


class QuartzBaseRequestHandler(RequestHandler):
    def render(self, template_name, **kwargs):
        super(QuartzBaseRequestHandler, self).render(template_name, version=__version__,
                                                     **kwargs)
