import logging
from urllib.parse import urlencode

import tornado.httpserver
import tornado.ioloop
import tornado.web

from mongoengine.errors import DoesNotExist

from eventer.models import User
import eventer.settings


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
        """
        Returns a dict that represent a default context for all rendered templates
        (Routes defined in :py:mod:`eventer.handlers.ui`)
        :return: dict
        """
        return {"settings": eventer.settings}


class AuthenticationRequiredHandler(DefaultContextRequestHandler):
    """
    Class for defining routes that need authentication - valid session token stored in database
    """

    def prepare(self):
        if not self.get_current_user():
            self.redirect("/login?{}".format(urlencode({"next": self.request.uri})))


class HttpPageHandler(DefaultContextRequestHandler):
    """
    Class for defining routes that do not need authentication and are public
    """
    pass


class ApiHandler(DefaultContextRequestHandler):
    """
    Class for defining routes that can be accessed by 3rd party clients or scripts. They must contain a valid value for
    the :py:data:`eventer.settings.API_REQUIRED_HEADER` header.
    """

    def get_current_user(self):
        req_header = self.request.headers.get(eventer.settings.API_REQUIRED_HEADER, None)
        if not req_header:
            return

        try:
            user = User.objects.get(api_token=req_header)
        except DoesNotExist:
            return
        else:
            return user
