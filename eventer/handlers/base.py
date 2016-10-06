import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web

from mongoengine.errors import DoesNotExist

from eventer.models import User


class DefaultContextRequestHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        session_cookie = self.get_secure_cookie("Session")
        # no session cookie is set
        if not session_cookie:
            return None
        else:
            session_cookie = session_cookie.decode()
            try:
                instance = User.objects.get(session_token=session_cookie)
            except DoesNotExist:
                # invalid session cookie
                return None
            else:
                return instance

    def get_default_context(self):
        return {
            "user_is_authenticated": self.get_current_user()
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
