import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost", database="relinquere_db", user="root", password=""
        )
        if connection.is_connected():
            print(
                f"Conexão com o banco de dados: {connection.database} estabelecida com sucesso"
            )
            return connection
    except Error as e:
        print(f"Erro ao tentar criar conexão com o banco de dados: {e};")


def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Conexão com o banco de dados encerrada.")
