from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from database import db
import json

dic = {
    'hola': 12345,
    'efef': 'adios',
    'clase': 234234
}

# GET: obtener
# DELETE: eliminar
# POST: crear
# PUT: actualizar

numero = dic['hola']

def hello_world(request): #"http://localhost:6543/producto
    url = request.url
    if request.method == 'GET':
        usuarios = db.engine.execute('SELECT * from usuarios')
        return Response(
            content_type = 'text/json',
            body = ''
        )
    elif request.method == 'POST':
        objeto = json.loads(request.json_body)
        objeto['nombre']
        
    elif request.method == 'DELETE':
        
    elif request.method == 'PUT':
        usurios = db.engine.execute('UPDATE usuarios set name = "Guti" where id = 0')
        
    bodyR = 'URL %s with name: %s' % (url, name) #URL http://localhost:6543/?name=guti with name: guti

    results = db.engine.execute('SELECT * from cocollector."Estados"')
    for estado in results:
        print(estado['id'])
        
    
    return Response(
        content_type = "text/plain",
        body = bodyR 
    ) # URL http://localhost:6543 with name guti

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/producto') # localhost:6543/
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
