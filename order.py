from pyramid.response import Response
from pyramid.request import Request
from sqlalchemy.engine import ResultProxy
from database import db
import json


def _get_order(request: Request) -> Response:
    order_id = request.params.get('id', -1)
    if order_id == -1:
        return Response(status=404)
    else:
        try:
            get_order = db.execute('SELECT * from cocollector."Orden" where "ID"= ' + order_id)
            return Response(status=200, body=json.dumps(get_order), content_type='text/json')
        except Exception:
            return Response(status=404)


def user_entry(request: Request):
    if request.method == 'GET':
        return _get_order(request)
    return Response()
