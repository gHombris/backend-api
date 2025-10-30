from flask import Blueprint, jsonify, request
from . import db
from .models import User

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint de login que consulta o banco de dados.
    """
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email e senha são obrigatórios"}), 400

    email = data.get('email')
    password = data.get('password')

    # NOVA LÓGICA: Consulta o banco pelo usuário
    user = User.query.filter_by(email=email).first()

    # Verifica se o usuário existe e se a senha está correta
    if not user or not user.check_password(password):
        return jsonify({"message": "Credenciais inválidas"}), 401

    # Retorna os dados do usuário usando a função to_dict()
    return jsonify(user.to_dict()), 200


@api_bp.route('/jogadora/<int:user_id>', methods=['GET'])
def get_jogadora(user_id):
    """
    Endpoint que retorna dados de uma jogadora pelo ID.
    """
    # NOVA LÓGICA: Busca o usuário pela chave primária (ID)
    user = db.session.get(User, user_id)

    if user:
        return jsonify(user.to_dict()), 200

    return jsonify({"message": "Jogadora não encontrada"}), 404


@api_bp.route('/ranking/semanal', methods=['GET'])
def get_ranking():
    """
    Endpoint que retorna o ranking de jogadoras ordenado por XP.
    """
    # NOVA LÓGICA: Consulta todos os usuários, ordena por XP (descendente)
    users = User.query.order_by(User.xp.desc()).all()

    # Converte a lista de objetos User em uma lista de dicionários
    ranking_data = []
    for user in users:
        ranking_data.append({
            "id": user.id,
            "nome": user.nome,
            "xp_semanal": user.xp,  # Usando XP total como semanal por enquanto
            "avatar": user.avatar_filename
        })

    return jsonify(ranking_data), 200