import re


def constraint_str_length_max(target, length):
    return len(target) < length


def constraint_str_length_min(target, length):
    return len(target) > length


def constraint_str_regex(target, regex):
    return re.match(regex, target)
