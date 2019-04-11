from pyramid.response import Response
from pyramid.request import Request
from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause

from database import db
import json


from query_to_json import to_json

import decimal, datetime

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def _get_order(request: Request) -> Response:
    if request.authenticated_userid is not None:
        try:
            order_data = request.params
            if 'id' in order_data:
                order_id = request.params.get('id', -1)
                if order_id == -1:
                    return Response(status=404)
                else:
                    try:
                        stmt: TextClause = text('SELECT * from cocollector."Orden" where "ID"= :id')
                        stmt = stmt.bindparams(id=order_id)

                        get_order: ResultProxy = db.execute(stmt)

                        return Response(status=200, body=json.dumps([dict(r) for r in get_order][0], default=alchemyencoder), content_type='text/json')
                    except Exception as e:
                        print(e)
                        return Response(status=404, content_type='text/plain')

            else:
                order_usuario = request.authenticated_userid
                if order_usuario == -1:
                    return Response(status=404)
                else:
                    try:
                        stmt: TextClause = text('SELECT * from cocollector."Orden" where "Usuario"= :usuario')
                        stmt = stmt.bindparams(usuario=order_usuario)

                        get_order: ResultProxy = db.execute(stmt)

                        return Response(status=200,
                                        body=json.dumps([dict(r) for r in get_order], default=alchemyencoder),
                                        content_type='text/json')
                    except Exception as e:
                        print(e)
                        return Response(status=404, content_type='text/plain')
        except Exception as e:
            print(e)
            return Response(status=404, content_type='text/plain')
    else:
        return Response(status=403, content_type='text/plain')


def _modify_order(request: Request) -> Response:
    if request.authenticated_userid:
        try:
            order_data = request.json_body
            order_stmt = text('SELECT * from cocollector."Orden" where "ID" = :id')
            order_stmt = order_stmt.bindparams(id=order_data['id'])
            get_order: ResultProxy = db.execute(order_stmt)
            order: dict = [dict(r) for r in get_order][0]
            alchemyencoder(order)
            if 'total' in order_data:
                order['Total'] = order_data['total']
            if 'estado' in order_data:
                order['Status'] = order_data['estado']
            if 'fechaPedido' in order_data:
                order['Fecha_pedido'] = order_data['fechaPedido']
            if 'direccion' in order_data:
                order['Direccion'] = order_data['direccion']
            if 'usuario' in order_data:
                order['Usuario'] = order_data['usuario']

            update_stmt = text(
                'UPDATE cocollector."Orden" SET "Total" = :total, "Status" = :estado, "Fecha_pedido" = :fechaPedido, "Direccion" = :direccion, "Usuario" = :usuario where "ID" = :id'
            ).bindparams(total=order['Total'], estado=order['Status'], fechaPedido=order['Fecha_pedido'], direccion=order['Direccion'], usuario=order['Usuario'], id=order['ID'])
            db.execute(update_stmt)

        except Exception as e:
            print(e)
            return Response(status=404, content_type='text/json')
    else:
        return Response(status=403, content_type='text/plain')


def _create_order(request: Request) -> Response:
    if request.authenticated_userid:
        try:
            order_data = request.json_body
            stmt: TextClause = text('INSERT into cocollector."Orden"("Total",'
                                    '"Status",'
                                    '"Fecha_pedido",'
                                    '"Direccion",'
                                    '"Usuario") VALUES (:total, :estado, NOW(), :direccion,'
                                    ':usuario) returning "ID"')
            stmt = stmt.bindparams(total=order_data['total'],
                                   estado=order_data['estado'],
                                   direccion=order_data['direccion'],
                                   usuario=order_data['usuario'])
            id_order_data = db.execute(stmt)
            id_order = [dict(r) for r in id_order_data][0]
            return Response(status=200,
                            content_type='application/json',
                            charset='utf-8',
                            body=json.dumps({'id': id_order['ID']}))
        except Exception as e:
            print(e)
            return Response(status=400)
    else:
        return Response(status=403, content_type='text/plain')


def _delete_order(request: Request) -> Response:

    if request.authenticated_userid:
        delete_data = request.json_body

        try:
            stmt: TextClause = text('DELETE FROM cocollector."Orden" where "ID" = :id').bindparams(id=delete_data['id'])
            db.execute(stmt)
            return Response(status=200, content_type='text/json')
        except Exception as e:
            print(e)
            return Response(status=404, content_type='text/plain')
    else:
        return Response(status=403, content_type='text/plain')


def order_entry(request: Request):
    if request.method == 'GET':
        return _get_order(request)
    elif request.method == 'POST':
        return _create_order(request)
    elif request.method == 'PUT':
        return _modify_order(request)
    elif request.method == 'DELETE':
        return _delete_order(request)
    elif request.method == 'OPTIONS':
        return Response(status=200, content_type='application/json', body=json.dumps({}), charset='utf-8')
    return Response(status=405, content_type='application/json')

