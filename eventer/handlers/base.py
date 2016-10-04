import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.web


class DefaultContextRequestHandler(tornado.web.RequestHandler):
    def get_default_context(self):
        return {
            "user_is_authenticated": False
        }


class AuthenticationRequiredHandler(DefaultContextRequestHandler):
    # noinspection PyMethodOverriding
    def initialize(self, database):
        self.database = database

    def prepare(self):
        pass


class HttpPageHandler(DefaultContextRequestHandler):
    pass


class ApiHandler(DefaultContextRequestHandler):
    pass
