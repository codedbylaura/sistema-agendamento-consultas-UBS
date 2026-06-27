from conexao import conectar


def listar_pacientes():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            cpf,
            data_nascimento,
            sexo,
            telefone,
            email,
            cartao_sus,
            endereco_id,
            ativo,
            criado_em,
            atualizado_em
        FROM paciente
        ORDER BY nome
    """)

    colunas = [desc[0] for desc in cursor.description]
    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    pacientes = [dict(zip(colunas, linha)) for linha in dados]

    return pacientes


def cadastrar_paciente(dados):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO paciente (
            nome,
            cpf,
            data_nascimento,
            sexo,
            telefone,
            email,
            cartao_sus,
            endereco_id
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (

        dados["nome"],
        dados["cpf"],
        dados["data_nascimento"],
        dados["sexo"],
        dados["telefone"],
        dados["email"],
        dados["cartao_sus"],
        dados["endereco_id"]

    ))

    conn.commit()

    cursor.close()
    conn.close()

    return True