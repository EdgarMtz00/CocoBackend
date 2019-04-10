from wsgiref.simple_server import make_server

from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.response import Response

from login import login_entry
from order import order_entry
from users import user_entry

from products import product_entry

from pyramid.renderers import JSON

import datetime
from category import category_entry


def hello_world(request):
    return Response(
        content_type="text/plain",
        body='hola'
    )


if __name__ == '__main__':
    json_renderer = JSON()

    def datetime_adapter(obj, request):
        return obj.isoformat()

    json_renderer.add_adapter(datetime.datetime, datetime_adapter)

    with Configurator() as config:
        # Pyramid requires an authorization policy to be active.
        config.set_authorization_policy(ACLAuthorizationPolicy())
        # Enable JWT authentication.
        config.include('pyramid_jwt')
        config.set_jwt_authentication_policy('secret')

        config.add_route('products', '/productos')  # localhost:6543/
        config.add_view(product_entry, route_name='products')
        config.add_renderer('json', json_renderer)
        config.add_route('users', '/usuarios')
        config.add_view(user_entry, route_name='users')
        config.add_route('order', '/orden')
        config.add_view(order_entry, route_name='order', renderer='json')
        config.add_route('login', '/login')
        config.add_view(login_entry, route_name='login')
        config.add_route('category', '/categorias')
        config.add_view(category_entry, route_name='category')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
