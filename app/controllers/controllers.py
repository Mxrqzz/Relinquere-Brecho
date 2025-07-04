import os
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app,
)
from werkzeug.utils import secure_filename
from app.database import create_connection, close_connection
from app.controllers.user import Usuario
from app.controllers.products import Products
from app.controllers.cart import Cart
from flask_bcrypt import Bcrypt
from functools import wraps

cripto = Bcrypt()

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def index():
    return render_template("index.html")


def register():
    if request.method == "POST":
        name = request.form["name"].capitalize().strip()
        email = request.form["email"].strip()
        senha = request.form["password"].strip()
        senha2 = request.form["passwordTwo"].strip()

        # Verifica se as senha e a confirmação estão iguais
        if senha != senha2:
            flash("As senhas não coincidem", "error")
            return render_template("register.html")
        senha_hash = cripto.generate_password_hash(senha).decode("utf-8")

        conexao = create_connection()
        if conexao:
            cursor = conexao.cursor()
            # Verifica se o email informado está já esta sendo utilizado
            cursor.execute("SELECT email FROM usuarios WHERE email =%s", (email,))
            existing_email = cursor.fetchone()

            if existing_email:
                flash("O E-mail informado já possui um cadastro", "error")
                return render_template("register.html")
        try:
            # salvando dados do usuario no banco de dados
            usuario = Usuario(name, email, senha_hash)
            usuario.salvar_dados()
            flash("Conta criada com sucesso", "success")
            return render_template("login.html")
        except Exception as e:
            flash(f"Erro ao tentar criar conta. {e}", "error")
            return render_template("register.html")
    return render_template("register.html")


def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        senha = request.form["password"].strip()

        conexao = create_connection()

        if conexao:
            cursor = conexao.cursor()
            # Verifica se o email informado existe no BD
            cursor.execute("SELECT * FROM usuarios WHERE email =%s", (email,))
            user = cursor.fetchone()

            if user:
                # Verifica se a senha está correta
                if cripto.check_password_hash(user[3], senha):
                    # Cria a sessão do sessão do usuario
                    session["user_id"] = user[0]
                    session["user_name"] = user[1]
                    session["user_email"] = user[2]
                    session["user_role"] = user[4]
                    Cart.sincronizar_carrinho()
                    close_connection(conexao)
                    return redirect(url_for("main.index_route"))
                else:
                    flash("Senha incorreta", "error")
            else:
                flash("E-mail não encontrado", "error")

    return render_template("login.html")


#! Logout
def logout():
    session.clear()
    flash("Desconectado com sucesso", "success")
    return redirect(url_for("main.login_route"))


#! Controle de sessão
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_role" not in session:
            flash("Você precisa está logado para acessar essa página", "error")
            return redirect(url_for("main.login_route"))

        elif session["user_role"] == "cliente":
            flash("Você não tem permissão para acessar essa página", "error")
            return redirect(url_for("main.shop_route"))

        return f(*args, **kwargs)

    return decorated_function


#! Shop
def shop():
    produtos = Products.listar_produtos()
    return render_template("shop.html", produtos=produtos)


#! Profile
def profile():
    return render_template("profile.html")


#! Cliente
@admin_required
def cliente():
    clientes = Usuario.listar_clientes()
    return render_template("clientes.html", clientes=clientes)


#! Produtos
@admin_required
def products():

    produtos = Products.listar_produtos()
    if request.method == "POST":
        nome = request.form["name"]
        description = request.form["description"]
        category = request.form["category"]
        size = request.form["size"]
        mark = request.form["mark"]
        color = request.form["color"]
        status = request.form["status"]
        obs = request.form["obs"]
        price = request.form["price"]
        imagem = request.files["img"]

        if imagem and allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)
            caminho_imagem = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            imagem.save(caminho_imagem)

        try:
            produto = Products(
                nome,
                description,
                category,
                size,
                mark,
                color,
                status,
                obs,
                price,
                filename,
            )
            produto.adicionar_produto()
            flash(f"Produto {nome} adicionado com sucesso.", "success")
            return redirect(url_for("main.products_route"))
        except Exception as e:
            flash(f"Erro ao tentar adicionar produto {e}", "error")
            return redirect(url_for("main.products_route"))

    return render_template("produtos.html", produtos=produtos)


def product_details(product_id):
    produto = Products.detalhes_produto(product_id)
    if not produto:
        flash("Produto não encontrado.", "error")
        return redirect(url_for("main.products_route"))

    return render_template("prodDetails.html", produto=produto)


#! Carrinho
def cart():
    carrinho_items = Cart.carrinho_items()
    total = sum([item[9] for item in carrinho_items])
    return render_template("carrinho.html", carrinhoItems=carrinho_items, total=total)


def add_to_cart(product_id):
    Cart.adicionar(product_id)
    return redirect(url_for("main.shop_route"))


def remove_from_cart(product_id):
    Cart.remover(product_id)
    return redirect(url_for("main.cart_route"))

#! Checkout
def checkout():
    return render_template('checkout.html')