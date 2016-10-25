from unittest import TestCase

from eventer.models import EventCategory, User
from eventer.fields import NumericEventField, StringEventField


class ObjectCreationTestCase(TestCase):
    def test_event_category_creation(self):
        category = EventCategory()

        category.name = "test_category"
        category.description = "test_description"
        category.user = self._get_test_user()

        field_1 = NumericEventField(name="log_message", description="log_description", required=True, max_value=20,
                                    min_value=0).as_dict()
        field_2 = StringEventField(name="msg2", description="msg2_descr", default="unknown", max_length=255).as_dict()

        category.fields = [field_1, field_2]

        category.save()

    def _get_test_user(self):
        pass
