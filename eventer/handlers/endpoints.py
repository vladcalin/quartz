import logging

import bcrypt
import simplejson
import tornado.gen
from mongoengine.errors import NotUniqueError

from eventer.handlers.base import HttpPageHandler
from eventer.models import User


class RegisterEndpointHandler(HttpPageHandler):
    @tornado.gen.coroutine
    def validate_username_and_email(self, username, email):
        result = []
        username_valid = User.objects(username=username).count()
        if username_valid:
            result.append("Username already taken")
        email_valid = User.objects(email=email).count()
        if email_valid:
            result.append("Email already in use")
        return result

    @tornado.gen.coroutine
    def persist_user(self, username, password, first_name, last_name, email):
        user_instance = User()
        user_instance.username = username
        user_instance.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user_instance.first_name = first_name
        user_instance.last_name = last_name
        user_instance.email = email
        user_instance.save()

        return user_instance

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

        if not email:
            errors.append("Email is mandatory")

        if not password:
            errors.append("Password is mandatory")

        if not first_name:
            errors.append("First name is mandatory")

        if not last_name:
            errors.append("Last name is mandatory")

        validate_result_errors = yield self.validate_username_and_email(username, email)
        if validate_result_errors:
            errors.extend(validate_result_errors)

        if errors:
            self.set_status(400, simplejson.dumps({"success": False, "errors": errors}))
            return

        registered_user = yield self.persist_user(username, password, first_name, last_name, email)
        logging.debug("Registered used: {}".format(registered_user.id))
        self.write(simplejson.dumps({"success": True}))
