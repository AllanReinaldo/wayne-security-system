import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuração da chave secreta via variável de ambiente (Segurança)
app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY", 
    "batman-wayne-enterprises-secret-key-2026"
)

CORS(app)
jwt = JWTManager(app)

# -------------------------------------------------------------------
# BANCO DE DADOS SIMULADO (Em memória)
# -------------------------------------------------------------------

# 1. Usuários Cadastrados com senhas tratadas por HASH (RBAC)
USUARIOS = {
    "bruce@wayne.com": {
        "nome": "Bruce Wayne",
        "senha": generate_password_hash("batman123"),
        "role": "admin"
    },
    "fox@wayne.com": {
        "nome": "Lucius Fox",
        "senha": generate_password_hash("tech123"),
        "role": "gerente"
    },
    "alfred@wayne.com": {
        "nome": "Alfred Pennyworth",
        "senha": generate_password_hash("tea123"),
        "role": "funcionario"
    }
}

# 2. Inventário de Recursos das Indústrias Wayne
RECURSOS = [
    {
        "id": 1,
        "nome": "Batmóvel (Tumbler)",
        "categoria": "Veículo",
        "nivel_acesso": "Restrito - Nível 3",
        "status": "Operacional",
        "localizacao": "Batcaverna - Setor A"
    },
    {
        "id": 2,
        "nome": "Batarangs de Liga de Titânio",
        "categoria": "Equipamento",
        "nivel_acesso": "Restrito - Nível 1",
        "status": "Estoque",
        "localizacao": "Arsenal Principal"
    },
    {
        "id": 3,
        "nome": "Sonar Global Gotham",
        "categoria": "Dispositivo",
        "nivel_acesso": "Restrito - Nível 3",
        "status": "Manutenção",
        "localizacao": "Torre Wayne - Subsolo 4"
    },
    {
        "id": 4,
        "nome": "Bat-Suit Mark V",
        "categoria": "Equipamento",
        "nivel_acesso": "Restrito - Nível 2",
        "status": "Operacional",
        "localizacao": "Batcaverna - Setor B"
    }
]

proximo_id_recurso = 5


# -------------------------------------------------------------------
# ROTAS DE AUTENTICAÇÃO (LOGIN & SEGURANÇA)
# -------------------------------------------------------------------

@app.route("/api/login", methods=["POST"])
def login():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido."}), 400

    email = dados.get("email")
    senha = dados.get("senha")

    usuario = USUARIOS.get(email)

    # Validação segura da senha via Hash
    if not usuario or not check_password_hash(usuario["senha"], senha):
        return jsonify({"erro": "Credenciais inválidas. Acesso negado!"}), 401

    # Criação do Token JWT com perfis e permissões do usuário
    claims_adicionais = {
        "nome": usuario["nome"],
        "role": usuario["role"]
    }
    access_token = create_access_token(identity=email, additional_claims=claims_adicionais)

    return jsonify({
        "mensagem": f"Bem-vindo(a), {usuario['nome']}!",
        "token": access_token,
        "usuario": {
            "nome": usuario["nome"],
            "email": email,
            "role": usuario["role"]
        }
    }), 200


# -------------------------------------------------------------------
# ROTAS DO DASHBOARD (PAINEL DE VISUALIZAÇÃO DE SEGURANÇA)
# -------------------------------------------------------------------

@app.route("/api/dashboard", methods=["GET"])
@jwt_required()
def obter_dashboard():
    total_recursos = len(RECURSOS)
    operacionais = sum(1 for r in RECURSOS if r["status"] == "Operacional")
    manutencao = sum(1 for r in RECURSOS if r["status"] == "Manutenção")
    estoque = sum(1 for r in RECURSOS if r["status"] == "Estoque")

    return jsonify({
        "status_sistema": "SISTEMA ONLINE - NÍVEL DE ALERTA VERDE",
        "estatisticas": {
            "total_recursos": total_recursos,
            "operacionais": operacionais,
            "manutencao": manutencao,
            "estoque": estoque
        },
        "ultimas_atividades": [
            "Acesso liberado no Setor A (Batcaverna)",
            "Manutenção agendada para o Sonar Global",
            "Inspeção de rotina do Batmóvel concluída"
        ]
    }), 200


# -------------------------------------------------------------------
# ROTAS DE GESTÃO DE RECURSOS (CRUD COMPLETO)
# -------------------------------------------------------------------

# 1. LISTAR RECURSOS
@app.route("/api/recursos", methods=["GET"])
@jwt_required()
def listar_recursos():
    return jsonify(RECURSOS), 200


# 2. CRIAR NOVO RECURSO
@app.route("/api/recursos", methods=["POST"])
@jwt_required()
def criar_recurso():
    global proximo_id_recurso
    dados = request.get_json()

    if not dados or not dados.get("nome") or not dados.get("categoria"):
        return jsonify({"erro": "Nome e Categoria são campos obrigatórios."}), 400

    novo_recurso = {
        "id": proximo_id_recurso,
        "nome": dados["nome"],
        "categoria": dados.get("categoria", "Equipamento"),
        "nivel_acesso": dados.get("nivel_acesso", "Restrito - Nível 1"),
        "status": dados.get("status", "Operacional"),
        "localizacao": dados.get("localizacao", "Torre Wayne")
    }

    RECURSOS.append(novo_recurso)
    proximo_id_recurso += 1

    return jsonify({"mensagem": "Recurso cadastrado com sucesso!", "recurso": novo_recurso}), 201


# 3. ATUALIZAR RECURSO EXISTENTE
@app.route("/api/recursos/<int:recurso_id>", methods=["PUT"])
@jwt_required()
def atualizar_recurso(recurso_id):
    dados = request.get_json()
    recurso = next((r for r in RECURSOS if r["id"] == recurso_id), None)

    if not recurso:
        return jsonify({"erro": "Recurso não encontrado."}), 404

    recurso["nome"] = dados.get("nome", recurso["nome"])
    recurso["categoria"] = dados.get("categoria", recurso["categoria"])
    recurso["nivel_acesso"] = dados.get("nivel_acesso", recurso["nivel_acesso"])
    recurso["status"] = dados.get("status", recurso["status"])
    recurso["localizacao"] = dados.get("localizacao", recurso["localizacao"])

    return jsonify({"mensagem": "Recurso atualizado com sucesso!", "recurso": recurso}), 200


# 4. REMOVER RECURSO
@app.route("/api/recursos/<int:recurso_id>", methods=["DELETE"])
@jwt_required()
def deletar_recurso(recurso_id):
    global RECURSOS
    recurso = next((r for r in RECURSOS if r["id"] == recurso_id), None)

    if not recurso:
        return jsonify({"erro": "Recurso não encontrado."}), 404

    RECURSOS = [r for r in RECURSOS if r["id"] != recurso_id]
    return jsonify({"mensagem": f"Recurso ID {recurso_id} removido com sucesso!"}), 200


if __name__ == "__main__":
    print("🦇 Servidor das Indústrias Wayne rodando em http://127.0.0.1:5000")
    app.run(debug=True, port=5000)