# seed.py
import json

# 1. Importamos a função 'create_app' e a instância 'db'
from app import create_app, db
# 2. Importamos o modelo 'User'
from app.models import User

# Dados de teste para nossas 8 jogadoras
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
    """
    Popula o banco de dados com os dados iniciais das jogadoras.
    """
    print("--- INICIANDO SEED SCRIPT ---")

    # 3. Criamos um "contexto de aplicação" para o script
    #    Isso é necessário para que o SQLAlchemy saiba com qual banco de dados se conectar.
    app = create_app()
    with app.app_context():
        # Limpa a tabela de usuários antes de adicionar novos
        # para evitar duplicatas se rodarmos o script várias vezes.
        db.session.query(User).delete()
        
        print("Criando novas usuárias...")
        
        # 4. Itera sobre nossos dados de teste e cria objetos User
        for data in jogadoras_data:
            # Cria uma nova instância do modelo User
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
            # Define a senha padrão "1234" para todas
            new_user.set_password('1234')
            
            # Adiciona a nova usuária à sessão do banco de dados
            db.session.add(new_user)

        # 5. "Commita" (salva) todas as novas usuárias no banco de dados de uma vez.
        try:
            db.session.commit()
            print(f"Sucesso! {len(jogadoras_data)} jogadoras foram adicionadas ao banco.")
        except Exception as e:
            db.session.rollback() # Desfaz as mudanças em caso de erro
            print(f"Erro ao adicionar jogadoras: {e}")

    print("\n--- SEED SCRIPT EXECUTADO COM SUCESSO ---")

if __name__ == '__main__':
    run_seed()