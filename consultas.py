import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
from flask_cors import CORS


CONFIGURACAO = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "ubs",
    "user":     "postgres",
    "password": "sua_senha"
}

def obter_conexao():
    return psycopg2.connect(**CONFIGURACAO, cursor_factory=RealDictCursor)

def criar_tabela():
    conn = obter_conexao()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id              SERIAL PRIMARY KEY,
            paciente_id     INTEGER NOT NULL REFERENCES pacientes(id),
            profissional_id INTEGER NOT NULL REFERENCES profissionais(id),
            data            DATE NOT NULL,
            hora            TIME NOT NULL,
            tipo            VARCHAR(100),
            status          VARCHAR(20) DEFAULT 'agendada',
            observacoes     TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


def criar_consulta(paciente_id, profissional_id, data, hora, tipo, status, observacoes):
    conn = obter_conexao()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO consultas (paciente_id, profissional_id, data, hora, tipo, status, observacoes)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (paciente_id, profissional_id, data, hora, tipo, status, observacoes))
    conn.commit()
    cur.close()
    conn.close()


def listar_consultas():
    conn = obter_conexao()
    cur = conn.cursor()
    cur.execute("SELECT * FROM consultas ORDER BY data, hora;")
    consultas = cur.fetchall()
    cur.close()
    conn.close()
    return consultas

def buscar_consulta(consulta_id):
    conn = obter_conexao()
    cur = conn.cursor()
    cur.execute("SELECT * FROM consultas WHERE id = %s;", (consulta_id,))
    consulta = cur.fetchone()
    cur.close()
    conn.close()
    return consulta


def atualizar_consulta(consulta_id, paciente_id, profissional_id, data, hora, tipo, status, observacoes):
    conn = obter_conexao()
    cur = conn.cursor()
    cur.execute("""
        UPDATE consultas
        SET paciente_id = %s, profissional_id = %s, data = %s, hora = %s,
            tipo = %s, status = %s, observacoes = %s
        WHERE id = %s;
    """, (paciente_id, profissional_id, data, hora, tipo, status, observacoes, consulta_id))
    conn.commit()
    cur.close()
    conn.close()


def excluir_consulta(consulta_id):
    conn = obter_conexao()
    cur = conn.cursor()
    cur.execute("DELETE FROM consultas WHERE id = %s;", (consulta_id,))
    conn.commit()
    cur.close()
    conn.close()


def relatorio_por_profissional():
    conn = obter_conexao()
    cur = conn.cursor()
    cur.execute("""
        SELECT pr.nome, COUNT(c.id) AS total
        FROM consultas c
        JOIN profissionais pr ON pr.id = c.profissional_id
        GROUP BY pr.nome
        ORDER BY total DESC;
    """)
    resultado = cur.fetchall()
    cur.close()
    conn.close()
    return resultado

def relatorio_por_data(data_inicio, data_fim):
    conn = obter_conexao()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.data, c.hora, c.status, pa.nome AS paciente, pr.nome AS profissional
        FROM consultas c
        JOIN pacientes pa ON pa.id = c.paciente_id
        JOIN profissionais pr ON pr.id = c.profissional_id
        WHERE c.data BETWEEN %s AND %s
        ORDER BY c.data, c.hora;
    """, (data_inicio, data_fim))
    resultado = cur.fetchall()
    cur.close()
    conn.close()
    return resultado


aplicacao = Flask(__name__)
CORS(aplicacao)

@aplicacao.get("/consultas")
def rota_listar():
    consultas = listar_consultas()
    return jsonify([dict(c) for c in consultas])

@aplicacao.get("/consultas/<int:consulta_id>")
def rota_buscar(consulta_id):
    consulta = buscar_consulta(consulta_id)
    if consulta is None:
        return jsonify({"erro": "Consulta nao encontrada"}), 404
    return jsonify(dict(consulta))

@aplicacao.post("/consultas")
def rota_criar():
    corpo = request.get_json()
    criar_consulta(
        corpo["paciente_id"], corpo["profissional_id"],
        corpo["data"], corpo["hora"], corpo["tipo"],
        corpo["status"], corpo["observacoes"]
    )
    return jsonify({"mensagem": "Consulta criada com sucesso."}), 201

@aplicacao.put("/consultas/<int:consulta_id>")
def rota_atualizar(consulta_id):
    corpo = request.get_json()
    atualizar_consulta(
        consulta_id,
        corpo["paciente_id"], corpo["profissional_id"],
        corpo["data"], corpo["hora"], corpo["tipo"],
        corpo["status"], corpo["observacoes"]
    )
    return jsonify({"mensagem": "Consulta atualizada com sucesso."})

@aplicacao.delete("/consultas/<int:consulta_id>")
def rota_excluir(consulta_id):
    excluir_consulta(consulta_id)
    return jsonify({"mensagem": "Consulta excluida com sucesso."})

@aplicacao.get("/relatorios/por-profissional")
def rota_relatorio_profissional():
    return jsonify([dict(r) for r in relatorio_por_profissional()])

@aplicacao.get("/relatorios/por-data")
def rota_relatorio_data():
    inicio = request.args.get("inicio")
    fim = request.args.get("fim")
    return jsonify([dict(r) for r in relatorio_por_data(inicio, fim)])

if __name__ == "__main__":
    criar_tabela()
    aplicacao.run(debug=True, port=5000)