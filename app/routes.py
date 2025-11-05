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
 # Pega o rank do usuário logado (enviado pelo app)
    # Ex: /api/ranking/semanal?rank=Ferro
    rank_filtro = request.args.get('rank')
    
    # Define o limite máximo de jogadoras
    LIMITE_MAXIMO = 16

    query = User.query

    # 1. Filtra pelo Rank (se foi fornecido)
    if rank_filtro:
        query = query.filter_by(rank=rank_filtro)
    
    # 2. Ordena por XP (descendente) e limita os resultados
    users = query.order_by(User.xp.desc()).limit(LIMITE_MAXIMO).all()

    # Converte a lista de objetos User em uma lista de dicionários
    ranking_data = []
    for user in users:
        ranking_data.append({
            "id": user.id,
            "nome": user.nome,
            "xp_semanal": user.xp,  # Usando XP total como semanal
            "avatar": user.avatar_filename
        })

    return jsonify(ranking_data), 200

def get_rank_for_xp(xp):
    if xp < 50:
        return 'Ferro'
    elif xp < 100:
        return 'Bronze'
    elif xp < 200:
        return 'Prata'
    elif xp < 400:
        return 'Ouro'
    elif xp < 800:
        return 'Rubi'
    elif xp < 1500:
        return 'Ametista'
    elif xp < 2500:
        return 'Safira'
    else:
        return 'Diamante'

@api_bp.route('/jogadora/atualizar_progresso', methods=['POST'])
def atualizar_progresso():
    """
    Endpoint que atualiza o progresso de uma jogadora (XP, treinos concluídos)
    """
    data = request.get_json()
    user_id = data.get('user_id')
    xp_ganho = data.get('xp_ganho', 0)

    if not user_id:
        return jsonify({"message": "ID do usuário é obrigatório"}), 400

    # Busca o usuário no banco
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    # Atualiza os dados
    novo_xp = (user.xp or 0) + xp_ganho
    user.xp = novo_xp
    
    # 2. Atualiza os treinos concluídos
    user.treinos_concluidos = (user.treinos_concluidos or 0) + 1
    
    # 3. VERIFICA E ATUALIZA O RANK 
    novo_rank = get_rank_for_xp(novo_xp)
    user.rank = novo_rank # Atualiza o rank no objeto do usuário

    # TODO: Implementar lógica de 'sequencia' (streak) futuramente

    try:
        db.session.commit()
        # Retorna o objeto User atualizado com o novo XP e (potencialmente) novo Rank
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao salvar progresso: {str(e)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao salvar progresso: {str(e)}"}), 500
@api_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint de criação de conta (Cadastro).
    Isso cumpre o requisito 'Create' do CRUD (Sprint 4) e SH-01 (Sprint 3).
    """
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    password = data.get('password')

    if not nome or not email or not password:
        return jsonify({"message": "Nome, email e senha são obrigatórios"}), 400

    # Verifica se o email já existe
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Este email já está em uso"}), 409 # 409 Conflict

    # Cria a nova usuária
    # Usamos os valores padrão do modelo para xp, rank, etc.
    new_user = User(
        nome=nome,
        email=email,
        avatar_filename='ana.png' # TODO: Adicionar um avatar padrão
    )
    # Define a senha com hash
    new_user.set_password(password) #

    try:
        db.session.add(new_user)
        db.session.commit()
        
        # Retorna os dados da nova usuária criada
        return jsonify(new_user.to_dict()), 201 # 201 Created
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao criar conta: {str(e)}"}), 500
@api_bp.route('/jogadora/atualizar_perfil', methods=['POST'])
def atualizar_perfil():
    """
    Endpoint de atualização de perfil (Nome e Avatar).
    Cumpre o requisito 'Update' do CRUD (Sprint 4) e SH-07 (Sprint 3).
    """
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({"message": "ID do usuário é obrigatório"}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    # Atualiza os campos se eles foram enviados no JSON
    if 'nome' in data:
        user.nome = data['nome']
    
    if 'avatar_filename' in data:
        user.avatar_filename = data['avatar_filename']

    try:
        db.session.commit()
        # Retorna o objeto User atualizado
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao atualizar perfil: {str(e)}"}), 500