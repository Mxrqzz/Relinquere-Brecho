from flask import session, flash
from app.database import create_connection, close_connection


class Cart:
    @staticmethod
    def carrinho_items():
        itens = []
        try:
            conexao = create_connection()
            if not conexao:
                raise Exception("Conexão com o banco de dados falhou.")

            cursor = conexao.cursor()

            # Se usuário logado, pega os produtos do banco
            if "user_id" in session:
                user_id = session["user_id"]
                cursor.execute(
                    "SELECT product_id FROM carrinhos WHERE user_id = %s", (user_id,)
                )
                carrinho = cursor.fetchall()
                produto_ids = [row[0] for row in carrinho]
            else:
                carrinho = session.get("cart", {})
                produto_ids = list(carrinho.keys())

            for produto_id in produto_ids:
                cursor.execute("SELECT * FROM produtos WHERE id = %s", (produto_id,))
                item = cursor.fetchone()
                if item:
                    itens.append(item)
                else:
                    print(f"Produto com ID {produto_id} não encontrado.")

        except Exception as e:
            print(f"Erro ao tentar listar produtos do carrinho: {e}")

        finally:
            cursor.close()
            close_connection(conexao)

        return itens

    @staticmethod
    def adicionar(produto_id):

        produto_id = str(produto_id)
        # Se o usuario estiver logado, salva o produto no banco de dados
        if "user_id" in session:
            user_id = session["user_id"]

            try:
                conexao = create_connection()
                if not conexao:
                    raise Exception("Erro ao conectar com o banco de dados.")
                cursor = conexao.cursor()

                cursor.execute(
                    "SELECT * FROM carrinhos WHERE user_id =%s AND product_id =%s",
                    (user_id, produto_id),
                )
                item_existing = cursor.fetchone()

                if item_existing:

                    flash("Esse produto já está no seu carrinho", "error")
                else:
                    cursor.execute(
                        "INSERT INTO carrinhos (user_id, product_id) VALUES (%s, %s)",
                        (
                            user_id,
                            produto_id,
                        ),
                    )
                    flash("Produto adicionado ao carrinho!", "success")
                    print("Produto adicionado ao carrinho!")
                conexao.commit()
            except Exception as e:
                print(f"error ao tentar adicionar produto ao carrinho: {e}")
                flash(f"error ao tentar adicionar produto ao carrinho: {e}", "error")
            finally:
                cursor.close()
                close_connection(conexao)
                print("A conexão com o banco de dados foi encerrada")

        # Se o usuario nao estiver logado salva o produto na sessao
        else:
            carrinho = session.get("cart", {})

            if produto_id in carrinho:
                flash("Esse produto já está no seu carrinho", "error")
            else:
                carrinho[produto_id] = 1
                session["cart"] = carrinho
                flash("Produto adicionado ao carrinho!", "success")

    @staticmethod
    def remover(produto_id):
        produto_id = str(produto_id)
        # Se o usuario estiver logado, remove o produto do banco de dados
        if "user_id" in session:
            user_id = session["user_id"]
            try:
                conexao = create_connection()
                if not conexao:
                    raise Exception("Erro ao conectar com o banco de dados.")
                cursor = conexao.cursor()
                cursor.execute(
                    "DELETE FROM carrinhos WHERE user_id =%s AND product_id =%s",
                    (user_id, produto_id),
                )
                flash("Produto removido do carrinho!", "success")
                conexao.commit()
            except Exception as e:
                flash(f"Erro ao tentar remover produto do carrinho: {e}", "error")
            finally:
                cursor.close()
                close_connection(conexao)
        # se não estiver logado remove da sessão
        else:
            carrinho = session.get("cart", {})
            if produto_id in carrinho:
                del carrinho[produto_id]
                session["cart"] = carrinho
                flash("Produto removido do carrinho", "error")
            else:
                flash("Produto não encontrado no carrinho", "error")

    @staticmethod
    def sincronizar_carrinho():
        if "user_id" not in session or "cart" not in session:
            return

        user_id = session["user_id"]
        carrinho_sessao = session["cart"]

        try:
            conexao = create_connection()
            if not conexao:
                raise Exception("Erro ao conectar com o banco de dados.")
            cursor = conexao.cursor()
            for produto_id in carrinho_sessao:
                cursor.execute(
                    "SELECT * FROM carrinhos WHERE user_id = %s AND product_id =%s",
                    (user_id, produto_id),
                )
                product_existing = cursor.fetchone()

                if not product_existing:
                    cursor.execute(
                        "INSERT INTO carrinhos (user_id, product_id) VALUES (%s, %s)",
                        (user_id, produto_id),
                    )
            conexao.commit()
            session.pop("cart")
            print("Carrinho da sessão sincronizado com o banco de dados.")
        except Exception as e:
            print(f"Erro ao sincronizar carrrinho: {e}")

        finally:
            cursor.close()
            close_connection(conexao)
