from flask import Blueprint

# Define Blueprints
auth_bp = Blueprint('auth', __name__)
menu_bp = Blueprint('menu', __name__)
orders_bp = Blueprint('orders', __name__)
admin_bp = Blueprint('admin', __name__)

from .cart import cart_bp

from . import auth, menu, orders, admin, cart
