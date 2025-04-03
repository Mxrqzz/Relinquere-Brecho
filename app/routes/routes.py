from flask import Blueprint
from app.controllers.controllers import *

bp = Blueprint("main", __name__)


@bp.route("/")
@bp.route("/index")
def index_route():
    return index()


@bp.route("/register", methods=["GET", "POST"])
def register_route():
    return register()


@bp.route("/login", methods=["GET", "POST"])
def login_route():
    return login()


@bp.route("/logout")
def logout_route():
    return logout()


@bp.route("/shop", methods=["GET"])
def shop_route():
    return shop()


@bp.route("/cart", methods=["GET"])
def cart_route():
    return cart()

@bp.route("/add_to_cart", methods=['POST'])
def add_to_cart_route():
    return add_to_cart()

@bp.route("/clientes", methods=["GET"])
def clientes_route():
    return cliente()


@bp.route("/products", methods=["GET", "POST"])
def products_route():
    return products()

@bp.route("/products/<int:product_id>")
def product_details_route(product_id):
    return product_details(product_id)