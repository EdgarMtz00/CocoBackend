import json
import datetime
from sqlalchemy.engine import ResultProxy


def to_json(query: ResultProxy):
    dic = []

    for row in query:
        print(row.keys()[0])
        for index, key in enumerate(row):
            dic.append({row.keys()[index]: key})
    return json.dumps(dic)
