# coding=utf-8
import tornado.web
from tornado.escape import json_decode, json_encode

from eventer.settings import EVENTER_TOKEN_HEADER


class GenericApiHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    def write_json(self, to_return):
        self.write(json_encode(to_return))

    def get_request_body_as_json(self):
        return json_decode(self.request.body)

    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)

        exc_class, exc, tb = kwargs.get("exc_info")

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
