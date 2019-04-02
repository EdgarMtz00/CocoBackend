from pyramid.response import Response
from pyramid.request import Request
from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause

from database import db
import json

from query_to_json import to_json


def _get_order(request: Request) -> Response:
    order_id = request.params.get('id', -1)
    if order_id == -1:
        return Response(status=404)
    else:
        try:
            stmt: TextClause = text('SELECT * from cocollector."Orden" where "ID" = :id')
            stmt = stmt.bindparams(id=order_id)

            get_order: ResultProxy = db.execute(stmt)
            result = get_order.fetchall()
            return Response(status=200, body=to_json(result), content_type='text/json')
        except Exception as e:
            print(e)
            return Response(status=404, content_type='text/plain')


def _create_order(request: Request) -> Response:
    try:
        order_data = request.json_body
        stmt: TextClause = text('INSERT into cocollector."Orden"("Total",'
                                '"Status",'
                                '"Fecha_pedido",'
                                '"Direccion",'
                                '"Usuario") VALUES (:total, :estado, :fecha_pedido, :direccion,'
                                ':usuario)')

        stmt = stmt.bindparams(total=order_data['total'], estado=order_data['estado'],
                               fecha_pedido=order_data['fechaPedido'], direccion=order_data['direccion'],
                               usuario=order_data['usuario'])
        db.execute(stmt)
        return Response(status=200)
    except Exception as e:
        print (e)
        return Response(status=400)


def _modify_order(request: Request) -> Response:
    try:
        order_data = request.json_body
        order_stmt = text('SELECT * from cocollector."Orden" where "ID" = :id').bindparams(id=order_data['id'])
        order: dict = json.loads(to_json(db.execute(order_stmt)))
        if 'total' in order_data:
            order['Total'] = order_data['total']
        if 'estado' in order_data:
            order['Estado'] = order_data['estado']
        if 'fecha_Pedido' in order_data:
            order['Fecha_pedido'] = order_data['fecha_Pedido']
        if 'direccion' in order_data:
            order['Direccion'] = order_data['direccion']
        if 'usuario' in order_data:
            order['Usuario'] = order_data['contrasena']

        update_stmt = text(
            'UPDATE cocollector."Orden" SET "Total" = :total, "Estado" = :estado, "Fecha_pedido" = :fecha_Pedido, "Direccion" = :direccion, "Usuario" = :usuario where "ID" = :id'
        ).bindparams(total=order['Total'], estado=order['Estado'], fecha_pedido=order['Fecha_pedido'], direccion=order['Direccion'], usuario=order['Usuario'])
        db.execute(update_stmt)

    except Exception as e:
        print(e)
        return Response(status=404, content_type='text/json')


def _delete_order(request: Request) -> Response:
    delete_data = request.json_body

    try:
        stmt: TextClause = text('DELETE FROM cocollector."Orden" where "ID" = :id').bindparams(id=delete_data['id'])
        db.execute(stmt)
        return Response(status=200, content_type='text/json')
    except Exception as e:
        print(e)
        return Response(status=404, content_type='text/plain')

def order_entry(request: Request):
    if request.method == 'GET':
        return _get_order(request)
    elif request.method == 'POST':
        return _create_order(request)
    elif request.method == 'PUT':
        return _modify_order(request)
    elif request.method == 'DELETE':
        return _delete_order(request)
    return Response(status=405, content_type='text/json')


