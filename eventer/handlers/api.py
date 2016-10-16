import tornado.gen

from eventer.handlers.base import ApiHandler
from eventer.models import EventCategory


class RegisterEventApiHandler(ApiHandler):
    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.set_status(403, "Invalid API authorization")
            return

        category = self.get_body_argument("category", None)
