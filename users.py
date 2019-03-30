from pyramid.response import Response
from pyramid.request import Request
from database import db
import json


def _get_user(request: Request):
    user_id = request.params.get('id', -1)
    if user_id == -1:
        try:
            get_all_users = db.execute('SELECT "Nombre", "Nombre_usuario", "Correo" from cocollector."Usuario"')
            return Response(status=200, body= json.dump(get_all_users), content_type='text/json')
        except Exception:
            return Response(status=404)
    else:
        try:
            get_user = db.execute('SELECT * from cocollector."Usuario" where id = ' + user_id)
            return Response(status=200, body= json.dump(get_user), content_type='text/json')
        except Exception:
            return Response(status=404)


def user_entry(request: Request):
    if request.method == 'GET':
        return user_entry()
    return Response()
