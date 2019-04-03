from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

from users import user_entry
from products import product_entry

def hello_world(request):
    return Response(
        content_type="text/plain",
        body='hola'
    )


if __name__ == '__main__':
    with Configurator() as config:
        #config.add_route('hello', '/hello')  # localhost:6543/
        #config.add_view(hello_world, route_name='hello')
        config.add_route('products', '/productos')  # localhost:6543/
        config.add_view(product_entry, route_name='products')
        config.add_route('users', '/usuarios')
        config.add_view(user_entry, route_name='users')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()

