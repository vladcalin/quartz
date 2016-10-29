from unittest import TestCase

from eventer.models import EventCategory, User, EventField, EventFieldConstraint


class ObjectCreationTestCase(TestCase):
    _test_user = None

    @classmethod
    def setUpClass(cls):
        cls._test_user = User()
        cls._test_user.username = "test"
        cls._test_user.set_password("test")
        cls._test_user.email = "test@test.test"
        cls._test_user.first_name = "test"
        cls._test_user.last_name = "test"
        cls._test_user.save()

    @classmethod
    def tearDownClass(cls):
        pass
        # cls._test_user.delete()

    def test_event_category_creation(self):
        category = EventCategory()

        category.name = "test_category"
        category.description = "test_description"
        category.user = self._get_test_user()

        constraint = EventFieldConstraint()
        constraint.type = EventFieldConstraint.Names.str_regex
        constraint.parameters = ["\w+"]

        event_field = EventField()
        event_field.name = "test"
        event_field.description = "testing"
        event_field.type = EventField.STRING
        event_field.constraints = [constraint]

        category.fields = [event_field]
        category.save()

        category.save()

    def _get_test_user(self):
        return self._test_user
