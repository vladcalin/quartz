# coding=utf-8
import tornado.web
from tornado.escape import json_decode, json_encode
from mongoengine import DoesNotExist, MultipleObjectsReturned

from eventer.settings import EVENTER_TOKEN_HEADER
from eventer.models import User, ApiToken
from eventer.errors import FatalErrorThatShouldNeverHappen, EventerError


class GenericApiHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    def write_json(self, to_return):
        self.write(json_encode(to_return))

    def get_request_body_as_json(self):
        return json_decode(self.request.body)

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

        self.write_json({
            "status": status_code,
            "info": info
        })


class ErrorHandler(GenericApiHandler, tornado.web.ErrorHandler):
    pass


class PublicApiHandler(GenericApiHandler):
    pass


class PrivateApiHandler(GenericApiHandler):
    def get_current_user(self):
        auth_token = self.request.headers.get(EVENTER_TOKEN_HEADER, None)
        if not auth_token:
            return

        try:
            user = User.objects.get(api_tokens__token=auth_token)
        except DoesNotExist:
            return
        except MultipleObjectsReturned:
            raise FatalErrorThatShouldNeverHappen("Multiple users with the same api_token found")
        else:
            return user

    def prepare(self):
        if not self.current_user:
            raise tornado.web.HTTPError(403, log_message="no valid API-token found.")
