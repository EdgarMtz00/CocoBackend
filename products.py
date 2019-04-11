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


def _get_product(request: Request) -> Response:
    product_id = request.params.get('id', -1)
    category_id = request.params.get('idCategoria', -1)
    try:
        if product_id != -1:
            stmt: TextClause = text('SELECT * FROM cocollector."Producto" WHERE "ID_Producto" = :id')
            stmt = stmt.bindparams(id=product_id)
        elif category_id != -1:
            stmt: TextClause = text('SELECT * FROM cocollector."Producto" WHERE "Categoria" = :categoryId')
            stmt = stmt.bindparams(categoryId=category_id)
        else:
            stmt: TextClause = text('SELECT * FROM cocollector."Producto"')

        get_product: ResultProxy = db.execute(stmt)
        return Response(status=200, body=json.dumps([dict(r) for r in get_product], default=alchemyencoder),
                        content_type='text/json')
    except Exception as e:
        print(e)
        return Response(status=404, content_type='text/plain')


def _create_product(request: Request) -> Response:
    try:
        product_data = request.json_body
        stmt: TextClause = text('INSERT INTO cocollector."Producto"("Descripcion",'
                                '"Nombre",'
                                '"Precio",'
                                '"Stock",'
                                '"Categoria") VALUES (:descripcion, :nombre, :precio, :stock, :categoria)')

        stmt = stmt.bindparams(descripcion=product_data['descripcion'],
                               nombre=product_data['nombre'],
                               precio=product_data['precio'],
                               stock=product_data['stock'],
                               categoria=product_data['categoria'])

        db.execute(stmt)

        return Response(status=200)
    except Exception:
        return Response(status=400)


def _modify_product(request: Request) -> Response:
    try:
        product_data = request.json_body

        stmt = text('SELECT * FROM cocollector."Producto" WHERE "ID_Producto" = :id')
        stmt = stmt.bindparams(id=product_data['id'])
        get_product: ResultProxy = db.execute(stmt)
        product: dict = [dict(r) for r in get_product][0]
        alchemyencoder(product)

        if 'descripcion' in product_data:
            product['Descripcion'] = product_data['descripcion']
        if 'nombre' in product_data:
            product['Nombre'] = product_data['nombre']
        if 'precio' in product_data:
            product['Precio'] = product_data['precio']
        if 'stock' in product_data:
            product['Stock'] = product_data['stock']
        if 'categoria' in product_data:
            product['Categoria'] = product_data['categoria']

        stmt = text('UPDATE cocollector."Producto" SET'
                    '"Descripcion" = :descripcion,'
                    '"Nombre" = :nombre,'
                    '"Precio" = :precio,'
                    '"Stock" = :stock,'
                    '"Categoria" = :categoria WHERE "ID_Producto" = :id')

        stmt = stmt.bindparams(descripcion=product['Descripcion'],
                               nombre=product['Nombre'],
                               precio=product['Precio'],
                               stock=product['Stock'],
                               categoria=product['Categoria'],
                               id=product['ID_Producto'])
        db.execute(stmt)

        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=404, content_type='text/json')


def _delete_product(request: Request) -> Response:
    try:
        product_data = request.json_body
        stmt = text('DELETE FROM cocollector."Producto" WHERE "ID_Producto" = :id')
        stmt = stmt.bindparams(id=product_data['id'])

        db.execute(stmt)

        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=404, content_type='text/json')


def product_entry(request: Request):
    if request.method == 'GET':
        return _get_product(request)
    elif request.method == 'POST':
        return _create_product(request)
    elif request.method == 'PUT':
        return _modify_product(request)
    elif request.method == 'DELETE':
        return _delete_product(request)
    return Response(status=405, content_type='text/json')
