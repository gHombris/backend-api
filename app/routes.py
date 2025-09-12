from flask import Blueprint, jsonify
from .models import JOGADORAS_DB, RANKING_SEMANAL_DB

# Cria um "Blueprint", uma forma de organizar um grupo de rotas relacionadas
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/jogadora/<int:user_id>', methods=['GET'])
def get_jogadora(user_id):
    """Retorna os dados de uma jogadora específica."""
    jogadora = next((j for j in JOGADORAS_DB if j["id"] == user_id), None)
    if jogadora:
        return jsonify(jogadora)
    return jsonify({"message": "Jogadora não encontrada"}), 404

@api_bp.route('/ranking/semanal', methods=['GET'])
def get_ranking():
    """Retorna a lista de jogadoras do ranking semanal."""
    # No futuro, aqui teríamos a lógica para ordenar por XP
    return jsonify(RANKING_SEMANAL_DB)