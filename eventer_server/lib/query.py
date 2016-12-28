import re
import datetime

from pypeg2 import Keyword, Literal, parse as pypeg_parse, Enum, K, name, Namespace, optional, csl, attr, word, List, \
    maybe_some, Symbol, whitespace, restline

"""
query :- "select \"" + queryname + "\" where " + clauses
queryname :- [a-zA-Z_\-0-9]+
clauses :- (single_clause) OR (single_clause + " and " + clauses)

single_clause :- (metadata_field_name OR regular_field_name) + " " + operator + " " + value

metadata_field_name :- "__timestamp__" OR "__source__"
regular_field_name :- "values__" + [a-zA-Z0-9_\-]+

operator :- "=" OR ">=" OR ">" OR "<" OR "<="
"""


# region Query grammar definition

class CategoryName(Symbol):
    regex = re.compile(r"[a-zA-Z0-9_\-]+")


class ClauseName(Symbol):
    regex = re.compile(r"\w+")


class ClauseOperator(Symbol):
    regex = re.compile(r"[^\s]{1,2}")
    grammar = Enum("=", "<", ">", ">=", "<=")


class ClauseValue(Symbol):
    regex = re.compile(r"(?:[\d\w]+)|('(?:[^']+)')|(\"(?:[^\"]+)\")")


class SingleClause(List):
    grammar = ClauseName, ClauseOperator, ClauseValue


class Clauses(List):
    grammar = SingleClause, maybe_some("and", SingleClause)


class Query(List):
    grammar = "select", maybe_some(whitespace), \
              '"', attr("category", re.compile("[^\"]+")), '"', maybe_some(whitespace), \
              'where', maybe_some(whitespace), attr("clauses", Clauses)


# endregion

class ParsedClause(object):
    relative_datetime_pattern = re.compile("(\d+)(h|m)")

    def __init__(self, name, operator, value):
        self.name = name
        self.operator = operator
        self.value = self._parse_value(value)

    def _parse_value(self, value):
        normalized_value = None

        # check if it is a string
        if value.startswith("'") and value.endswith("'"):
            normalized_value = value.strip("'")
        if value.startswith('"') and value.endswith('"'):
            normalized_value = value.strip('"')
        if normalized_value:
            return normalized_value

        # check if int
        try:
            normalized_value = int(value)
        except ValueError:
            pass
        else:
            return normalized_value

        # check if bool
        if value.lower() == "true":
            normalized_value = True
        if value.lower() == "false":
            normalized_value = False
        if normalized_value:
            return normalized_value

        # check if datetime relative to today
        check = self.relative_datetime_pattern.match(value)
        if check:
            if check.group(2) == "h":
                relative_delta = datetime.timedelta(hours=int(check.group(1)))
            elif check.group(2) == "m":
                relative_delta = datetime.timedelta(minutes=int(check.group(1)))
            else:
                raise ValueError("Invalid relative time delta suffix: {}".format(check.group(2)))
            normalized_value = datetime.datetime.now() - relative_delta

        if normalized_value:
            return normalized_value

        raise ValueError("Could not determine the type of value: {}".format(value))

    def __repr__(self):
        return "<{0} {1} {2}>".format(self.name, self.operator, self.value)


class ParsedQuery(object):
    def __init__(self, category_name, clauses=None):
        self.category_name = category_name
        self.clauses = []
        if clauses:
            for clause in clauses:
                self.add_clause(clause)

    def add_clause(self, clause):
        if isinstance(clause, dict):
            name = clause["name"]
            operator = clause["op"]
            value = clause["value"]
        elif isinstance(clause, tuple):
            name, operator, value = clause
        elif isinstance(clause, ParsedClause):
            self.clauses.append(clause)
            return
        else:
            raise ValueError("Not supported clause of type {}".format(type(clause).__name__))

        self.clauses.append(ParsedClause(name, operator, value))

    def __repr__(self):
        return "<ParsedQuery category={0} clauses={1}>".format(self.category_name, self.clauses)


class QueryParser(object):
    def __init__(self):
        pass

    def parse_query(self, query_string):
        parsed = pypeg_parse(query_string, Query)

        clauses = [{"name": str(x[0]), "op": str(x[1]), "value": str(x[2])} for x in parsed.clauses]

        parsed_query = ParsedQuery(parsed.category)
        for clause in clauses:
            parsed_query.add_clause(clause)

        return parsed_query


if __name__ == '__main__':
    query = 'select "relevant_events" where __timestamp__ >= 1h and field_1 == "hello" and field_2>=0'
    parse_result = QueryParser().parse_query(
        'select "relevant_events" where __timestamp__ >= 2h and __timestamp__ <= 1h and field_1 '
        '= "hello world" and field_2 = 0 and field_3 = \'qweqweqwe\'')

    print(parse_result)
