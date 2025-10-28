# app/__init__.py
import os  # <<< Adicione este import
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)  # <<< Adicione instance_relative_config=True
    CORS(app)

    # --- CONFIGURAÇÃO DO SQLITE ---
    # Garante que a pasta 'instance' exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Define o caminho para o arquivo do banco de dados SQLite
    # Ele será criado dentro de uma pasta chamada 'instance' na raiz do projeto
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'skillher.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # -----------------------------

    db.init_app(app)

    from . import routes
    app.register_blueprint(routes.api_bp)

    return app