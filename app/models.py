# app/models.py
from . import db
# Importamos as funções de hashing de senha
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Aumentamos o tamanho para hashes longos
    xp = db.Column(db.Integer, default=0)
    rank = db.Column(db.String(50), default='Ferro')
    treinos_concluidos = db.Column(db.Integer, default=0)
    sequencia = db.Column(db.Integer, default=0)
    avatar_filename = db.Column(db.String(100), nullable=True)

    # --- NOVAS FUNÇÕES ADICIONADAS ---

    def set_password(self, password):
        """Cria um hash seguro para a senha fornecida."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Converte o objeto User em um dicionário para ser enviado como JSON."""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'xp': self.xp,
            'rank': self.rank,
            'treinos_concluidos': self.treinos_concluidos,
            'sequencia': self.sequencia,
            'avatar_filename': self.avatar_filename
            # Não inclua o 'password_hash' por segurança!
        }

    def __repr__(self):
        return f'<User {self.nome} (ID: {self.id})>'