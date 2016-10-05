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
    """
    Class for defining routes that need authentication - valid auth token stored in database
    """
    # noinspection PyMethodOverriding
    def initialize(self, database):
        self.database = database

    def prepare(self):
        pass


class HttpPageHandler(DefaultContextRequestHandler):
    """
    Class for defining routes that do not need authentication and are public
    """
    pass


class ApiHandler(DefaultContextRequestHandler):
    pass
