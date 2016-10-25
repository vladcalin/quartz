from eventer.base import BaseEventField


class NumericEventField(BaseEventField):
    def __init__(self, name, description, required=False,
                 default=None, max_value=None, min_value=None):
        self.name = name
        self.description = description
        self.required = required
        self.default = default
        self.max_value = max_value
        self.min_value = min_value

    def value_is_valid(self, value):
        pass

    @classmethod
    def from_dict(cls, dictionary):
        if dictionary["type"] != "int":
            raise ValueError("Invalid 'type' "
                             "for NumericEventField")

        instance = cls(name=dictionary["name"],
                       description=["description"],
                       required=dictionary["constraints"]["required"],
                       default=dictionary["constraints"]["default"],
                       min_value=dictionary["constraints"]["min_value"],
                       max_value=dictionary["constraints"]["max_value"])
        return instance

    def as_dict(self):
        return {
            "type": "int",
            "name": self.name,
            "description": self.description,
            "constraints": {
                "default": self.default,
                "required": self.required,
                "max_value": self.max_value,
                "min_value": self.min_value
            }
        }

    def sanitize(self, value):
        try:
            return int(value)
        except ValueError as e:
            raise ValueError("Unable to convert '{}' to int".format(value)) from e


class StringEventField(BaseEventField):
    def __init__(self, name, description, required=False, default=None, min_length=None, max_length=None, regex=None):
        self.name = name
        self.description = description
        self.required = required
        self.default = default
        self.min_length = min_length
        self.max_length = max_length
        self.regex = regex

    def as_dict(self):
        return {
            "type": "str",
            "name": self.name,
            "description": self.description,
            "constraints": {
                "default": self.default,
                "required": self.required,
                "max_length": self.max_length,
                "min_length": self.min_length,
                "regex": self.regex
            }
        }

    def value_is_valid(self, value):
        pass

    def from_dict(self, dictionary):
        pass

    def sanitize(self, value):
        return str(value)
