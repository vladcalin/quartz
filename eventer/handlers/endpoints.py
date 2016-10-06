import logging

import bcrypt
import simplejson
import tornado.gen
from mongoengine.errors import NotUniqueError, DoesNotExist

from eventer.handlers.base import HttpPageHandler
from eventer.models import User


class RegisterEndpointHandler(HttpPageHandler):
    @tornado.gen.coroutine
    def validate_username_and_email(self, username, email):
        result = []
        username_valid = User.objects(username__exact=username).count()
        if username_valid:
            result.append("Username already taken")
        email_valid = User.objects(email__exact=email).count()
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
        registered_user.session_token = User.generate_session_token()
        registered_user.save()
        self.set_secure_cookie("Session", registered_user.session_token)
        self.set_header("Content-Type", "application/json")
        self.write(simplejson.dumps({"success": True}))


class AuthenticationEndpointHandler(HttpPageHandler):
    @tornado.gen.coroutine
    def validate_username_and_password(self, username, password):
        try:
            user = User.objects.get(username)
        except DoesNotExist:
            return False
        else:
            return bcrypt.checkpw(password.decode(), user.password)

    @tornado.gen.coroutine
    def post(self):
        if self.get_current_user():
            self.set_status(403, "Already authenticated")
            return

        username = self.get_body_arguments("username")
        password = self.get_body_arguments("password")
        is_valid = yield self.validate_username_and_password(username, password)
        if is_valid:
            new_token = User.generate_session_token()
            target_user = User.objects.get(username=username)
            target_user.session_token = new_token
            target_user.save()
            self.set_secure_cookie("Session", new_token)
            self.redirect("/", permanent=True)
        else:
            self.set_status(403, "Invalid username or password")


class LogoutEndpointHandler(HttpPageHandler):
    @tornado.gen.coroutine
    def post(self):
        current_user = self.get_current_user()
        current_user.session_token = None
        current_user.save()
        self.redirect("/", permanent=True)

    @tornado.gen.coroutine
    def get(self):
        self.post()
