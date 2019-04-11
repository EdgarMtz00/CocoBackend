import json

from pyramid.response import Response, FileResponse
from pyramid.request import Request
from pyramid_storage.exceptions import FileNotAllowed
from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause

from database import db

def _upload_image(request: Request):
    if(request.authenticated_userid):
        image_data = request.json_body
        try:
            stmt:  TextClause = text('INSERT INTO "Imagen"("Ruta", "Producto") values (:ruta, :producto)')
            stmt = stmt.bindparams(ruta=image_data['ruta'], producto=image_data['id'])
            db.execute(stmt)
            return Response(status=200)
        except FileNotAllowed:
            request.session.flash("Archivo no permitido")
        return Response(status=200)
    else:
        return Response(status=403, content_type='text/plain')


def _get_image(request: Request):
    try:
        id_imagen = request.json_body['id']
        stmt: TextClause = text('SELECT "Ruta" FROM "Imagen" where "ID" = :id')
        stmt = stmt.bindparams(id=id_imagen)
        result = db.execute(stmt)
        imagen = [dict(r) for r in result][0]
        return Response(status=200,
                        body=json.dumps({'ruta': imagen['Ruta']}),
                        content_type='application/json',
                        charset='utf-8')
    except Exception as e:
        print(e)
        return Response(status=400)


def product_image_entry(request: Request):
    if request.method == 'POST':
        return _upload_image(request)
    if request.method == 'GET':
        return _get_image(request)
    return Response(status=405, content_type='text/json')