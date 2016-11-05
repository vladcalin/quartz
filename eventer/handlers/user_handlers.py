# coding=utf-8
import logging
from concurrent.futures.thread import ThreadPoolExecutor

from mongoengine import Q
import tornado.gen
import tornado.web
from tornado.escape import json_decode
import bcrypt

from eventer.handlers.base import PublicApiHandler
from eventer.models import User

_executor = ThreadPoolExecutor(8)


class UserCreationApiHandler(PublicApiHandler):
    _req_fields = [
        "username", "password", "email", "first_name", "last_name"
    ]

    @tornado.gen.coroutine
    def username_and_email_are_valid(self, username, email):
        user = yield _executor.submit(self.query_for_user, username, email)
        if not user:
            return

        errors = []
        if user.username == username:
            errors.append("username taken")
        if user.email == email:
            errors.append("email already in use")

        raise tornado.web.HTTPError(400, ", ".join(errors))

    def query_for_user(self, username, email):
        users = list(User.objects.filter(Q(username=username) or Q(email=email)))
        if users:
            return users[0]
        else:
            return None

    def persist_user(self, username, password, email, first_name, last_name):
        user = User()
        user.username = username
        user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user

    def get_parameter(self, request, param):
        return request.get(param, None)

    @tornado.gen.coroutine
    def post(self):
        post_data = self.get_request_body_as_json()

        self.check_request_parameters(post_data)

        username = post_data.get("username")
        email = post_data.get("email")
        password = post_data.get("password")
        first_name = post_data.get("first_name")
        last_name = post_data.get("last_name")
        yield self.username_and_email_are_valid(username=username, email=email)

        user_instance = yield _executor.submit(self.persist_user,
                                               username, password, email, first_name, last_name)
        self.write_json(user_instance)

    def check_request_parameters(self, post_data):
        errors = []
        for field in self._req_fields:
            if field not in post_data:
                errors.append(field)
        if errors:
            raise tornado.web.HTTPError(400, log_message="The following parameters are missing: {}".format(
                ", ".join(errors)))
