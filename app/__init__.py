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

    # --- LÓGICA DE BANCO DE DADOS ATUALIZADA PARA DEPLOY ---
    
    # 1. Busca a DATABASE_URL da variável de ambiente (que a Vercel vai fornecer)
    db_uri = os.environ.get('DATABASE_URL')

    if db_uri:
        # Se estiver no Vercel (produção), ele vai usar o Postgres
        # (O Postgres do Vercel não gosta de "postgres://", ele prefere "postgresql://")
        if db_uri.startswith("postgres://"):
            db_uri = db_uri.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    else:
        # 2. Se não achar (rodando local), ele continua usando o SQLite
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'skillher.db')}"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # --------------------------------------------------

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models
    from . import routes
    app.register_blueprint(routes.api_bp)

    return app