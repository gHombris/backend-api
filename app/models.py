# app/models.py
# Este arquivo define as estruturas das nossas tabelas no banco de dados
# usando classes Python e o SQLAlchemy ORM.

# Importamos a instância 'db' que criamos no __init__.py
from . import db


class User(db.Model):
    """
    Representa a tabela 'user' no banco de dados.
    Cada atributo da classe corresponde a uma coluna na tabela.
    """
    # Define o nome da tabela explicitamente (opcional, mas boa prática)
    __tablename__ = 'user'

    # Coluna 'id': Chave primária, tipo Inteiro.
    # primary_key=True: Marca esta coluna como a chave única da tabela.
    id = db.Column(db.Integer, primary_key=True)

    # Coluna 'nome': Tipo String (texto), com tamanho máximo de 80 caracteres.
    # nullable=False: Indica que esta coluna não pode ficar vazia (obrigatória).
    nome = db.Column(db.String(80), nullable=False)

    # Coluna 'email': Tipo String, tamanho máximo 120.
    # unique=True: Garante que não podem existir dois usuários com o mesmo email.
    # nullable=False: Obrigatório.
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Coluna 'password_hash': Tipo String, tamanho 128.
    # Armazenaremos a senha criptografada (hash), nunca a senha original.
    # nullable=False: Obrigatório.
    password_hash = db.Column(db.String(128), nullable=False)

    # Coluna 'xp': Tipo Inteiro.
    # default=0: Se não for especificado ao criar um usuário, o valor inicial será 0.
    xp = db.Column(db.Integer, default=0)

    # Coluna 'rank': Tipo String, tamanho 50.
    # default='Ferro': Valor inicial para novos usuários.
    rank = db.Column(db.String(50), default='Ferro')

    # Coluna 'treinos_concluidos': Tipo Inteiro, valor inicial 0.
    treinos_concluidos = db.Column(db.Integer, default=0)

    # Coluna 'sequencia': Tipo Inteiro, valor inicial 0.
    sequencia = db.Column(db.Integer, default=0)

    # --- Campos que não tínhamos nos mocks, mas são úteis ---

    # Coluna 'avatar_filename': Tipo String.
    # Armazenaremos apenas o nome do arquivo da imagem (ex: 'luana_pereira.png').
    # nullable=True: Permite que o usuário não tenha um avatar.
    avatar_filename = db.Column(db.String(100), nullable=True)

    # Método __repr__ (opcional): Define como o objeto User será exibido
    # se o imprimirmos (útil para depuração).
    def __repr__(self):
        return f'<User {self.nome} (ID: {self.id})>'

# --- PODEMOS ADICIONAR OUTROS MODELOS AQUI NO FUTURO ---
# Exemplo: Tabela de Treinos, Tabela de Conquistas, etc.
# class Training(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     category = db.Column(db.String(50))
#     difficulty = db.Column(db.String(50))
#     video_filename = db.Column(db.String(100))