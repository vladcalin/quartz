import tornado.gen
from http.client import BAD_REQUEST, FORBIDDEN

from mongoengine.errors import DoesNotExist

from eventer.handlers.base import ApiHandler
from eventer.models import EventCategory


class RegisterEventApiHandler(ApiHandler):
    @tornado.gen.coroutine
    def get_event_category(self, category_id):
        try:
            category = EventCategory.objects.get(id=category_id)
        except DoesNotExist:
            return None
        else:
            return category

    @tornado.gen.coroutine
    def post(self):
        if not self.current_user:
            self.set_status(FORBIDDEN, "Invalid API authorization")
            return

        category = self.get_body_argument("category", None)
        if not category:
            self.set_status(BAD_REQUEST, "Missing mandatory argument 'category'")

