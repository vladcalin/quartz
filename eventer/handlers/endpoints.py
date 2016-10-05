import logging

import tornado.gen

from eventer.handlers.base import HttpPageHandler


class RegisterEndpointHandler(HttpPageHandler):
    @tornado.gen.coroutine
    def validate_username(self, username):
        return True

    @tornado.gen.coroutine
    def validate_email(self, email):
        return True

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        username = self.get_body_argument("username", None)
        password = self.get_body_argument("password", None)
        first_name = self.get_body_argument("first_name", None)
        last_name = self.get_body_argument("last_name", None)
        email = self.get_body_argument("email", None)

        errors = []
        if not username:
            errors.append("Username is mandatory")
        else:
            username_is_unique = yield from self.validate_username(username)
            if not username_is_unique:
                errors.append("Username taken")

        if not email:
            errors.append("Email is mandatory")
        else:
            email_is_unique = yield from self.validate_email(email)
            if not email_is_unique:
                errors.append("Email already in use")

        if not password:
            errors.append("Password is mandatory")

        if not first_name:
            errors.append("First name is mandatory")

        if not last_name:
            errors.append("Last name is mandatory")
