from app.database import create_connection, close_connection
from flask import session


class Usuario:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def salvar_dados(self):
        try:
            conexao = create_connection()

            if conexao:
                cursor = conexao.cursor()
                sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
                values = (self.name, self.email, self.password)
                cursor.execute(sql, values)
                conexao.commit()

            print(f"Usuario: {self.name}, cadastrado com sucesso.")
        except Exception as e:
            print(f"Erro ao tentar cadastrar usuario: {e}.")
        finally:
            cursor.close()
            close_connection(conexao)
            print("A Conexão com o banco de dados foi encerrada.")

    @staticmethod
    def listar_clientes():
        try:
            conexao = create_connection()
            if not conexao:
                raise Exception("Conexão com o banco de dados falhou")

            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE role = 'cliente'")
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar clientes {e}")
            return []
        finally:
            close_connection(conexao)



