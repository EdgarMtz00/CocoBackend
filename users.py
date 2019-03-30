from pyramid.response import Response
from pyramid.request import Request
from sqlalchemy.engine import ResultProxy
from database import db
import json


def _get_user(request: Request) -> Response:
    user_id = request.params.get('id', -1)
    if user_id == -1:
        return Response(status=404)
    else:
        try:
            get_user = db.execute('SELECT * from cocollector."Usuario" where "ID"= ' + user_id)
            return Response(status=200, body=json.dumps(get_user), content_type='text/json')
        except Exception:
            return Response(status=404)


def user_entry(request: Request):
    if request.method == 'GET':
        return _get_user(request)
    return Response()
