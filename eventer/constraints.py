# coding=utf-8
import re
import abc

from eventer.errors import ConstraintViolationError


class BaseFieldConstraint(abc.ABC):
    @abc.abstractmethod
    def check(self, value):
        """
        Check whether the value violates a constraint or not
        :param value: the value to validate
        :return: None
        :raises: ConstraintViolationError on fail
        """
        pass


class StringMaxLengthConstraint(BaseFieldConstraint):
    def __init__(self, max_length):
        self.max_length = max_length

    def check(self, value):
        if len(value) > self.max_length:
            raise ConstraintViolationError("Maximum length exceeded")


class StringMinLengthConstraint(BaseFieldConstraint):
    def __init__(self, min_length):
        self.min_length = min_length

    def check(self, value):
        if len(value) < self.min_length:
            raise ConstraintViolationError("Lower length that exceeded")


class StringRegexConstraint(BaseFieldConstraint):
    def __init__(self, regex):
        self.regex = re.compile(regex)

    def check(self, value):
        if not self.regex.match(value):
            raise ConstraintViolationError("Expression does not match given regex")


class ConstraintNames:
    """
    Supported constraints names.
    """
    str_len_min = "str_len_min"
    str_len_max = "str_len_max"
    str_regex = "str_regex"

    all = [
        str_len_min, str_len_max, str_regex
    ]


class ConstraintFactory:
    _values = {
        ConstraintNames.str_len_max: StringMaxLengthConstraint,
        ConstraintNames.str_len_min: StringMinLengthConstraint,
        ConstraintNames.str_regex: StringRegexConstraint,
    }

    @classmethod
    def get(cls, name, arguments):
        return cls._values[name](*arguments)
