from app.database import create_connection, close_connection


class Cart:
    @staticmethod
    def carrinho_items(cart):
        itens = []
        try:
            conexao = create_connection()
            if not conexao:
                raise Exception("Conexão com o banco de dados falhou.")

            cursor = conexao.cursor()

            for produto_id in cart:
                cursor.execute("SELECT * FROM produtos WHERE id=%s", (produto_id,))
                item = cursor.fetchone()

                if item:
                    itens.append(item)
                else:
                    print("Item não encontrado")

            return itens

        except Exception as e:
            print(f"Erro ao tentar listar produtos do carrinho: {e}")
            return itens

        finally:
            cursor.close()
            close_connection(conexao)
