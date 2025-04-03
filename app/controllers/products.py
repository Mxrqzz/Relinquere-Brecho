from app.database import create_connection, close_connection


class Products:
    def __init__(
        self, name, description, category, size, mark, color, status, obs, price, img
    ):

        self.name = name
        self.description = description
        self.category = category
        self.size = size
        self.mark = mark
        self.color = color
        self.status = status
        self.obs = obs
        self.price = price
        self.img = img

    def adicionar_produto(self):
        try:
            conexao = create_connection()

            if conexao:
                cursor = conexao.cursor()
                sql = """INSERT INTO produtos (nome, descricao, categoria, tamanho, marca, cor, estado, obs, preco, imagem) 
                VALUES (%s, %s,%s,%s,%s, %s,%s,%s,%s,%s)"""
                values = (
                    self.name,
                    self.description,
                    self.category,
                    self.size,
                    self.mark,
                    self.color,
                    self.status,
                    self.obs,
                    self.price,
                    self.img,
                )

                cursor.execute(sql, values)
                conexao.commit()
            print(f"Produto {self.nome} cadastrado com sucesso.")

        except Exception as e:
            print(f"Erro ao tentar cadastrar o produto: {e}.")
        finally:
            cursor.close()
            close_connection(conexao)
            print("A Conexão com o banco de dados foi encerrada.")
            
    @staticmethod
    def listar_produtos():
        try:
            conexao = create_connection()
            if not conexao:
                raise Exception("Conexão com o banco de dados falhou")
            
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM produtos")
            produtos = cursor.fetchall()
            if produtos:
                return produtos
        except Exception as e:
            print(f"Erro ao listar produtos {e}")
            return []
        finally:
            close_connection(conexao)