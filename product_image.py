import json
from sqlalchemy.engine import ResultProxy
from pyramid.response import Response, FileResponse
from pyramid.request import Request
from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause

from database import db

#Método para subir la una imagen de un producto.
def _upload_image(request: Request):
    if(request.authenticated_userid):
        image_data = request.json_body
        try:
            stmt:  TextClause = text('INSERT INTO "Imagen"("Ruta", "Producto") values (:ruta, :producto)')
            stmt = stmt.bindparams(ruta=image_data['ruta'], producto=image_data['id'])
            db.execute(stmt)
            return Response(status=200)
        except Exception as e:
            request.session.flash("Archivo no permitido")
        return Response(status=200)
    else:
        return Response(status=403, content_type='text/plain')

#Método para obtener cuatro imágenes random junto con la id y categoría de su producto.
def _get_image():
    try:
        stmt: TextClause = text('SELECT "Ruta", "Producto", "Categoria" FROM cocollector."Imagen" '
                                'JOIN cocollector."Producto" ON '
                                'cocollector."Imagen"."Producto" = cocollector."Producto"."ID_Producto" '
                                'ORDER BY RANDOM() LIMIT 5')
        result: ResultProxy = db.execute(stmt)

        return Response(status=200, body=json.dumps([dict(r) for r in result]), 
                        content_type='application/json', charset='utf-8')
    except Exception as e:
        print(e)
        return Response(status=400)

#Dependiendo del método usado en el request se ejecuta alguno de los 4 métodos disponibles para producto.      
def product_image_entry(request: Request):
    if request.method == 'POST':
        return _upload_image(request)
    if request.method == 'GET':
        return _get_image()
    elif request.method == 'OPTIONS':
        return Response(status=200, content_type='application/json', body=json.dumps({}), charset='utf-8')
    return Response(status=405, content_type='text/json')