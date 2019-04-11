from wsgiref.simple_server import make_server

from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.response import Response

from login import login_entry
from order import order_entry
from requisition import req_entry
from users import user_entry
from product_image import product_image_entry
from products import product_entry

from pyramid.renderers import JSON

import datetime
from category import category_entry


def hello_world(request):
    return Response(
        content_type="text/plain",
        body='hola'
    )

def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)

if __name__ == '__main__':
    json_renderer = JSON()

    def datetime_adapter(obj, request):
        return obj.isoformat()

    json_renderer.add_adapter(datetime.datetime, datetime_adapter)

    with Configurator() as config:
        config.add_subscriber(add_cors_headers_response_callback, NewRequest)
        # Pyramid requires an authorization policy to be active.
        config.set_authorization_policy(ACLAuthorizationPolicy())
        # Enable JWT authentication.
        config.include('pyramid_jwt')

        config.set_jwt_authentication_policy('secret')

        config.add_route('products', '/productos')  # localhost:6543/
        config.add_view(product_entry, route_name='products')
        config.add_route('product_image', '/producto-imagen')
        config.add_view(product_image_entry, route_name='product_image')
        config.add_renderer('json', json_renderer)
        config.add_route('users', '/usuarios')
        config.add_view(user_entry, route_name='users')
        config.add_route('order', '/orden')
        config.add_route('req', '/pedido')
        config.add_view(req_entry, route_name='req')
        config.add_view(order_entry, route_name='order', renderer='json')
        config.add_route('login', '/login')
        config.add_view(login_entry, route_name='login')
        config.add_route('category', '/categorias')
        config.add_view(category_entry, route_name='category')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
