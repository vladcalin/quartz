# coding=utf-8
from concurrent.futures.thread import ThreadPoolExecutor
import logging
import http.client

import tornado.web
import tornado.gen
from tornado.escape import json_decode, json_encode
from mongoengine import DoesNotExist, MultipleObjectsReturned

from eventer.settings import EVENTER_TOKEN_HEADER, EVENTER_SESSION_COOKIE
from eventer.models import User, ApiToken, Session
from eventer.errors import FatalErrorThatShouldNeverHappen, EventerError

_executor = ThreadPoolExecutor(8)


class GenericApiHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    def write_json(self, to_return):
        self.write(json_encode(to_return))

    def get_request_body_as_json(self):
        return json_decode(self.request.body)

    # def initialize(self, *args, **kwargs):
    #     logging.error((args, kwargs))

    def write_error(self, status_code, **kwargs):

        exc_class, exc, tb = kwargs.get("exc_info")

        if issubclass(exc_class, EventerError) \
                and not exc_class == FatalErrorThatShouldNeverHappen:
            status_code = 400

        self.set_status(status_code)
        if hasattr(exc, "log_message"):
            info = exc.log_message
        else:
            info = str(exc)

        if not info:
            info = http.client.responses[status_code]

        self.write_json({
            "status": status_code,
            "info": info
        })


class ErrorHandler(GenericApiHandler, tornado.web.ErrorHandler):
    pass


class PublicApiHandler(GenericApiHandler):
    pass


class PrivateApiHandler(GenericApiHandler):
    def _get_user_by_api_token(self, api_token):
        if not api_token:
            return
        try:
            user = User.objects.get(api_tokens__token=api_token)
        except DoesNotExist:
            return
        except MultipleObjectsReturned:
            raise FatalErrorThatShouldNeverHappen("Multiple users with the same api_token found")
        else:
            return user

    def _get_user_by_session_cookie(self, cookie):
        if isinstance(cookie, bytes):
            cookie = cookie.decode()
        logging.info(cookie)
        if not cookie:
            return

        try:
            session = Session.objects.get(token=cookie)
            logging.info(session)
        except DoesNotExist:
            return None
        else:
            return session.user

    def get_current_user(self):
        auth_token = self.request.headers.get(EVENTER_TOKEN_HEADER)
        session_cookie = self.get_secure_cookie(EVENTER_SESSION_COOKIE)

        user = self._get_user_by_api_token(auth_token)
        if user:
            return user

        user = self._get_user_by_session_cookie(session_cookie)
        if user:
            return user

        raise tornado.web.HTTPError(403, "Unauthorized")

    def prepare(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403, log_message="no valid API-token found.")
