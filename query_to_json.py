import json
from sqlalchemy.engine import ResultProxy


def to_dict(query: ResultProxy):
    dic = []

    for row in query:
        print(row.keys()[0])
        for index, key in enumerate(row):
            dic.append({row.keys()[index]: key})


def to_json(query: ResultProxy):
    return json.dumps(to_dict(query))
