# app/__init__.py
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    # --- LÓGICA DE BANCO DE DADOS SOMENTE PRODUÇÃO ---
    
    # 1. Busca a DATABASE_URL da variável de ambiente.
    db_uri = os.environ.get('DATABASE_URL')

    # 2. SE NÃO ACHAR, O APP VAI FALHAR (o que é bom, pois nos diz o erro)
    if not db_uri:
        raise RuntimeError("FATAL: A variável de ambiente DATABASE_URL não está configurada.")

    # 3. Converte a URL do Supabase para o formato que o SQLAlchemy gosta
    if db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql://", 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # --------------------------------------------------

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models
    from . import routes
    app.register_blueprint(routes.api_bp)

    return app