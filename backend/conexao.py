import psycopg2
from config import HOST, PORTA, BANCO, USUARIO, SENHA


def conectar():
    """
    Cria uma conexão com o banco de dados PostgreSQL.
    """

    conexao = psycopg2.connect(
        host=HOST,
        port=PORTA,
        database=BANCO,
        user=USUARIO,
        password=SENHA
    )

    return conexao


# remover depois

if __name__ == "__main__":
    try:
        conexao = conectar()
        print("Conexão realizada com sucesso!")
        conexao.close()
    except Exception as erro:
        print("Erro ao conectar:")
        print(erro)