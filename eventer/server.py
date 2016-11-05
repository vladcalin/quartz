import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.log

from eventer.settings import SERVER_HOST, SERVER_PORT
from eventer.handlers.user_handlers import UserCreationApiHandler
from eventer.handlers.base import ErrorHandler


def make_app(app_settings):
    return tornado.web.Application([
        # user-related api
        (r"/api/users/create", UserCreationApiHandler),  # POST, public

    ], **app_settings)


if __name__ == '__main__':
    settings = {
        "static_path": os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
        "template_path": os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
        "cookie_secret": "!$FF#@T&%NRfWG%$h6J45t2#!deDSBn7j5^g43dQWadFDBn7^7%$r",
        "xsrf_cookies": False,
        "default_handler_class": ErrorHandler
    }
    tornado.log.enable_pretty_logging()

    server = tornado.httpserver.HTTPServer(make_app(settings))
    server.bind(SERVER_PORT)
    server.start()
    tornado.ioloop.IOLoop.current().start()
