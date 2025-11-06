import json
from app import create_app, db
from app.models import User

jogadoras_data = [
    { 'id': 1, 'nome': "Emilly", 'email': "emilly@skillher.com", 'xp': 80, 'rank': 'Bronze', 'treinos_concluidos': 12, 'sequencia': 5, 'avatar_filename': 'emilly.png' },
    { 'id': 2, 'nome': "Ana", 'email': "ana@skillher.com", 'xp': 50, 'rank': 'Bronze', 'treinos_concluidos': 8, 'sequencia': 3, 'avatar_filename': 'ana.png' },
    { 'id': 3, 'nome': "Maria", 'email': "maria@skillher.com", 'xp': 45, 'rank': 'Ferro', 'treinos_concluidos': 7, 'sequencia': 2, 'avatar_filename': 'maria.png' },
    { 'id': 4, 'nome': "Tatiana", 'email': "tatiana@skillher.com", 'xp': 35, 'rank': 'Ferro', 'treinos_concluidos': 5, 'sequencia': 1, 'avatar_filename': 'tatiana.png' },
    { 'id': 5, 'nome': "Ester", 'email': "ester@skillher.com", 'xp': 35, 'rank': 'Ferro', 'treinos_concluidos': 4, 'sequencia': 0, 'avatar_filename': 'ester.png' },
    { 'id': 6, 'nome': "Andreia", 'email': "andreia@skillher.com", 'xp': 30, 'rank': 'Ferro', 'treinos_concluidos': 3, 'sequencia': 0, 'avatar_filename': 'andreia.png' },
    { 'id': 7, 'nome': "Monique", 'email': "monique@skillher.com", 'xp': 15, 'rank': 'Ferro', 'treinos_concluidos': 1, 'sequencia': 1, 'avatar_filename': 'monique.png' },
    { 'id': 8, 'nome': "Luana Pereira", 'email': "luana@skillher.com", 'xp': 10, 'rank': 'Ferro', 'treinos_concluidos': 0, 'sequencia': 0, 'avatar_filename': 'luana_pereira.png' }
]

def run_seed():
    print("--- INICIANDO SEED SCRIPT ---")
    app = create_app()
    with app.app_context():
        
        # <<< LÓGICA DE SEED ATUALIZADA (NÃO DESTRUTIVA) >>>
        jogadoras_criadas = 0
        for data in jogadoras_data:
            # 1. Verifica se a jogadora já existe pelo email
            user_existente = User.query.filter_by(email=data['email']).first()
            
            # 2. Se não existir, crie-a
            if not user_existente:
                new_user = User(
                    id=data['id'],
                    nome=data['nome'],
                    email=data['email'],
                    xp=data['xp'],
                    rank=data['rank'],
                    treinos_concluidos=data['treinos_concluidos'],
                    sequencia=data['sequencia'],
                    avatar_filename=data['avatar_filename']
                )
                new_user.set_password('1234')
                db.session.add(new_user)
                jogadoras_criadas += 1
                print(f"Criando: {data['nome']}")
            else:
                print(f"Ignorando (já existe): {data['nome']}")

        if jogadoras_criadas > 0:
            try:
                db.session.commit()
                print(f"Sucesso! {jogadoras_criadas} novas jogadoras foram adicionadas.")
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao adicionar jogadoras: {e}")
        else:
            print("Nenhuma nova jogadora para adicionar.")

    print("\n--- SEED SCRIPT EXECUTADO COM SUCESSO ---")

if __name__ == '__main__':
    run_seed()