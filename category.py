from pyramid.response import Response
from pyramid.request import Request
from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause
from database import db
import json


def get_category(request):
    try:
        stmt: TextClause = text('SELECT * FROM cocollector."Categoria"')
        get_product: ResultProxy = db.execute(stmt)
        return Response(status=200, body=json.dumps([dict(r) for r in get_product]), content_type='text/json')
    except Exception as e:
        print(e)
        return Response(status=404, content_type='text/plain')


def create_category(request):
    try:
        category_data = request.json_body
        stmt: TextClause = text('INSERT INTO cocollector."Categoria" ("Nombre", "Descripcion") values (:nombre, :descr)')
        stmt = stmt.bindparams(descr=category_data['descripcion'], nombre=category_data['nombre'])
        db.execute(stmt)
        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=404, content_type='text/plain')


def delete_category(request):
    try:
        category_id = request.json_body
        stmt: TextClause = text('DELETE FROM cocollector."Categoria" WHERE "ID" = :id')
        stmt = stmt.bindparams(id=category_id['id'])
        db.execute(stmt)
        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=404, content_type='text/plain')


def category_entry(request):
    if request.method == 'GET':
        return get_category(request)
    if request.method == 'POST':
        return create_category(request)
    if request.method == 'DELETE':
        return delete_category(request)
