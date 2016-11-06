# coding=utf-8
import logging
from concurrent.futures.thread import ThreadPoolExecutor

from mongoengine import Q, DoesNotExist
import tornado.gen
import tornado.web
from tornado.escape import json_decode
import bcrypt

from eventer.handlers.base import PublicApiHandler, PrivateApiHandler
from eventer.models import User, Session
from eventer.settings import EVENTER_SESSION_COOKIE

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
        user.set_password(password)
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
        user_instance.generate_api_token()
        self.write_json(user_instance.to_dict())

    def check_request_parameters(self, post_data):
        errors = []
        for field in self._req_fields:
            if field not in post_data:
                errors.append(field)
        if errors:
            raise tornado.web.HTTPError(400, log_message="The following parameters are missing: {}".format(
                ", ".join(errors)))


class AuthenticateUserHandler(PublicApiHandler):
    def get_user_by_username(self, username):
        try:
            user = User.objects.get(username=username)
        except DoesNotExist:
            return None
        else:
            return user

    @tornado.gen.coroutine
    def post(self):
        data = self.get_request_body_as_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise tornado.web.HTTPError(400, log_message="missing required parameter")

        user = yield _executor.submit(self.get_user_by_username, username)
        if not user:
            raise tornado.web.HTTPError(403, "Invalid username or password")
        if user.verify_password(password):
            session = user.create_new_session()
            self.set_secure_cookie(EVENTER_SESSION_COOKIE, str(session.token))
            self.write_json(user.to_dict())
        else:
            raise tornado.web.HTTPError(403, log_message="Invalid username or password")


class LogoutUserHandler(PrivateApiHandler):
    @tornado.gen.coroutine
    def post(self):
        self.current_user.revoke_session(self.get_secure_cookie(EVENTER_SESSION_COOKIE))
        self.set_secure_cookie(EVENTER_SESSION_COOKIE, "")
        self.write_json({
            "status": "success",
            "info": "You have been logged out."
        })


class GetUserInfoHandler(PrivateApiHandler):
    @tornado.gen.coroutine
    def get(self):
        self.write_json(self.current_user.to_dict())


class CreateNewTokenHandler(PrivateApiHandler):
    def post(self):
        self.current_user.generate_api_token()
        self.write_json(self.current_user.to_dict())


class RevokeTokenHandler(PrivateApiHandler):
    def post(self):
        token = self.get_request_body_as_json()["token"]
        self.current_user.revoke_api_token(token)
        self.write_json(self.current_user.to_dict())
