from pyramid.response import Response
from pyramid.request import Request
from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause

from database import db
import json

from query_to_json import to_json


def _get_user(request: Request) -> Response:
    user_id = request.params.get('id', -1)
    if request.authenticated_userid:
        user_id = request.authenticated_userid
    if user_id == -1:
        return Response(status=404)
    else:
        try:
            stmt: TextClause = text('SELECT "ID", '
                                    '"Nombre_usuario",'
                                    '"Correo",'
                                    '"Nombre", '
                                    '"Apellido_paterno", '
                                    '"Apellido_materno",'
                                    '"Tipo" from cocollector."Usuario" where "ID" = :id')
            stmt = stmt.bindparams(id=user_id)
            result = db.execute(stmt)

            return Response(status=200,
                            body=json.dumps([dict(r) for r in result][0]),
                            content_type='application/json',
                            charset='utf-8')
        except Exception as e:
            print(e)
            return Response(status=404, content_type='text/plain')


def _create_user(request: Request) -> Response:
    try:
        user_data = request.json_body
        print(user_data)
        stmt: TextClause = text('INSERT into cocollector."Usuario"("Nombre_usuario",'
                                '"Correo",'
                                '"Contrasena",'
                                '"Nombre",'
                                '"Apellido_paterno",'
                                '"Apellido_materno",'
                                '"Tarjeta_credito",'
                                '"Fecha_Expiracion",'
                                '"Tipo") VALUES (:nombre_usuario, :correo, :contrasena, '
                                ":nombre, :apellido_paterno, :apellido_materno, :tarjeta, :fecha_expiracion, 'Usuario' )")
        nombre_usuario = user_data['nombreUsuario']
        stmt = stmt.bindparams(nombre_usuario=nombre_usuario, correo=user_data['correo'],
                               contrasena=user_data['contrasena'], nombre=user_data['nombre'],
                               apellido_paterno=user_data['apellidoPaterno'],
                               apellido_materno=user_data['apellidoMaterno'], tarjeta=user_data['tarjeta'],
                               fecha_expiracion=user_data['fechaExpiracion'])

        db.execute(stmt)
        stmt = text('SELECT * FROM cocollector."Usuario" where "Nombre_usuario" = :username')
        stmt = stmt.bindparams(username=nombre_usuario)
        result = db.execute(stmt)
        user_data = [dict(r) for r in result][0]
        token = request.create_jwt_token(user_data['ID'])
        return Response(status=200, charset='utf-8', content_type='application/json', body=json.dumps({'token': token}))
    except Exception as e:
        print(e)
        return Response(status=400)


def _modify_user(request: Request) -> Response:
    if request.authenticated_userid is None:
        return Response(status=401, body=json.dumps({}), content_type='application/json')
    try:

        user_data = request.json_body
        user_stmt = text('SELECT * from cocollector."Usuario" where "ID" = :id').bindparams(id=request.authenticated_userid)
        user: dict = json.loads(to_json(db.execute(user_stmt)))
        if 'nombre' in user_data:
            user['Nombre'] = user_data['nombre']
        if 'apellidoPaterno' in user_data:
            user['Apellido_paterno'] = user_data['apellidoPaterno']
        if 'apellidoMaterno' in user_data:
            user['Apellido_materno'] = user_data['apellidoMaterno']
        if 'nombreDeUsuario' in user_data:
            user['Nombre_usuario'] = user_data['nombreDeUsuario']
        if 'correo' in user_data:
            user['Correo'] = user_data['correo']
        if 'contrasena' in user_data:
            user['Contrasena'] = user_data['contrasena']

        update_stmt = text(
            'UPDATE cocollector."Usuario" SET "Nombre" = :nombre, "Apellido_paterno" = :apellido_paterno, "Apellido_materno" = :apellido_materno, "Nombre_usuario" = :nombre_usuario, "Correo" = :correo, "Contrasena" = :contrasena where "ID" = :id'
        ).bindparams(nombre=user['Nombre'], apellido_paterno=user['Apellido_paterno'],
                     nombre_usuario=user['Nombre_usuario'], correo=user['Correo'], contrasena=user['Contrasena'],
                     apellido_materno=user['Apellido_materno'])
        db.execute(update_stmt)

    except Exception as e:
        print(e)
        return Response(status=404, content_type='text/json')


def user_entry(request: Request):
    if request.method == 'GET':
        return _get_user(request)
    elif request.method == 'POST':
        return _create_user(request)
    elif request.method == 'PUT':
        return _modify_user(request)
    elif request.method == 'OPTIONS':
        return Response(status=200, content_type='application/json', body=json.dumps({}), charset='utf-8')
    return Response(status=405, content_type='text/json')
