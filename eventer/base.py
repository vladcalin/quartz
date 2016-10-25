import abc


class BaseEventField(abc.ABC):
    @abc.abstractmethod
    def as_dict(self):
        """
        Returns the field as a dictionary with JSON-serializable values.

        :return: dictionary with the given parameters
        """
        pass

    @abc.abstractmethod
    def from_dict(self, dictionary):
        """
        Creates an event field object from the given dictionary.

        :param dictionary:
        :return:
        """
        pass

    @abc.abstractmethod
    def value_is_valid(self, value):
        """
        Validates **value** based on the constraints of the current
        object.

        :param value: an object to be validated by the field rules and constraints
        :return: True if the the value is valid, False otherwise
        """
        pass

    @abc.abstractmethod
    def sanitize(self, value):
        """
        Converts the given value to the appropriate data type required by the field

        :param value: An object to be converted to the proper data type
        :return:
        """
