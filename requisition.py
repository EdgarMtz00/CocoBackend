from pyramid.response import Response
from pyramid.request import Request
from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause

from database import db
import json

import decimal, datetime

def alchemyencoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def _get_req(request: Request) -> Response:
    req_id = request.params.get('id', -1)
    if request.authenticated_userid:
        req_id = request.authenticated_userid
    if req_id == -1:
        return Response(status=404)
    else:
        try:
            stmt: TextClause = text('SELECT * from cocollector."Pedido" where "ID"= :id')
            stmt = stmt.bindparams(id=req_id)

            get_req: ResultProxy = db.execute(stmt)

            return Response(status=200,
                            body=json.dumps([dict(r) for r in get_req][0],
                                            default=alchemyencoder), content_type='text/json')
        except Exception as e:
            print(e)
            return Response(status=404, content_type='text/plain')


def _create_req(request: Request) -> Response:
    try:
        req_data = request.json_body
        for req in req_data:
            stmt: TextClause = text('INSERT into cocollector."Pedido"("Total",''"Cantidad",'
                                    '"Orden",''"Producto") VALUES (:total, :cantidad, :orden, :producto)')
            stmt = stmt.bindparams(total=req['total'], cantidad=req['cantidad'],
                               orden=req['orden'], producto=req['producto'])
            db.execute(stmt)
        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=400)


def _modify_req(request: Request) -> Response:
    if request.authenticated_userid is None:
        return Response(status=401, body=json.dumps({}), content_type='application/json')
    try:
        req_data = request.json_body
        req_stmt = text('SELECT * from cocollector."Pedido" where "ID" = :id').bindparams(id=request.authenticated_userid)
        req: dict = json.loads((db.execute(req_stmt)))
        if 'total' in req_data:
            req['Total'] = req_data['total']
        if 'cantidad' in req_data:
            req['Cantidad'] = req_data['cantidad']
        if 'orden' in req_data:
            req['Orden'] = req_data['orden']
        if 'producto' in req_data:
            req['Producto'] = req_data['producto']

        update_stmt = text('UPDATE cocollector."Pedido" SET "Total" = :total, '
                           '"Cantidad" = :cantidad, "Orden" = :orden, '
                           '"Producto" = :producto where "ID" = :id'
                           ).bindparams(total=req['Total'], cantidad=req['Cantidad'],
                                        orden=req['Orden'], producto=req['Producto'])
        db.execute(update_stmt)
    except Exception as e:
        print(e)
        return Response(status=404, content_type='text/json')



def _delete_req(request: Request) -> Response:
    delete_data = request.json_body
    try:
        stmt: TextClause = text('DELETE FROM cocollector."Pedido" where "ID" = :id').bindparams(id=delete_data['id'])

        delete_req: ResultProxy = db.execute(stmt)

        return Response(status=200,
                        body=json.dumps([dict(r) for r in delete_req][0],
                                        default=alchemyencoder), content_type='text/json')
    except Exception as e:
        print(e)
        return Response(status=404, content_type='text/plain')


def req_entry(request: Request):
    if request.method == 'GET':
        return _get_req(request)
    elif request.method == 'POST':
        return _create_req(request)
    elif request.method == 'PUT':
        return _modify_req(request)
    elif request.method == 'DELETE':
        return _delete_req(request)
    elif request.method == 'OPTIONS':
        return Response(status=200, content_type='application/json', body=json.dumps({}), charset='utf-8')
    return Response(status=405, content_type='text/json')
