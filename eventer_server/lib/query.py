import re


class QueryParseError(Exception):
    pass


class QueryTokens:
    def __init__(self, operation, category, operator, interval):
        self.operation = operation
        self.category = category
        self.operator = operator
        self.interval = interval


class QueryParser(object):
    query_regex = re.compile(
        '(?P<operation>[^\s]+)\s*"(?P<category>[^"]+)"\s(?P<operator>[^\s]+)\s(?P<interval>[^\s]+)')

    def __init__(self):
        pass

    def parse_query(self, query_string):
        items = self.query_regex.match(query_string)
        if not items:
            raise QueryParseError("Unable to parse query: {}".format(query_string))

        return QueryTokens(
            operation=items.group(1), category=items.group(2), operator=items.group(3),
            interval=items.group(4)
        )


if __name__ == '__main__':
    query = 'select "Category1" >= 24h'
    items = QueryParser().parse_query(query)

    query = 'select "events_category_01" >= 15m'
    items = QueryParser().parse_query(query)
