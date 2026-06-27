from flask import Blueprint, jsonify, request
from services.paciente_service import listar_pacientes, cadastrar_paciente

pacientes_bp = Blueprint("pacientes", __name__)

@pacientes_bp.route("/pacientes", methods=["GET"])
def get_pacientes():

    pacientes = listar_pacientes()

    return jsonify({
        "status": "ok",
        "data": pacientes
    })

@pacientes_bp.route("/pacientes", methods=["POST"])
def post_paciente():

    dados = request.get_json()

    if not dados:
        return jsonify({
            "status": "erro",
            "message": "Nenhum dado enviado."
        }), 400

    if not dados.get("nome"):
        return jsonify({
            "status": "erro",
            "message": "O nome é obrigatório."
        }), 400

    if not dados.get("cpf"):
        return jsonify({
            "status": "erro",
            "message": "O CPF é obrigatório."
        }), 400

    cadastrar_paciente(dados)

    return jsonify({
        "status": "ok",
        "message": "Paciente cadastrado com sucesso!"
    }), 201
