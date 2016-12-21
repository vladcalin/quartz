import re


class QueryParseError(Exception):
    pass


class QueryTokens:
    def __init__(self, category, filters):
        self.category = category
        self.filters = filters


class QueryParser(object):
    value_regex = re.compile(
        r'(?P<key>[^\s]+?)\s*(?P<operator>[><=]+)\s*(?P<value>[^\s]+)'
    )
    query_regex = re.compile(
        'select\s*"(?P<category>[^"]+)"\s*where\s(?P<filter>.+)'
    )

    def __init__(self):
        pass

    def parse_query(self, query_string):
        items = self.query_regex.match(query_string)
        if not items:
            raise QueryParseError("Unable to parse query: {}".format(query_string))

        category = items.group(1)
        filter_string = items.group(2)

        items = self.value_regex.findall(filter_string)
        if not items:
            raise QueryParseError("Unable to parse query: {}. Cannot extract filters".format(query_string))

        return QueryTokens(category=category, filters=items)


if __name__ == '__main__':
    query = 'select "relevant_events" where __timestamp__ >= 1h and field_1="hello" and field_2>=0'
    items = QueryParser().parse_query(query)
