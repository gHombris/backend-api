from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app) # Habilita o CORS para o app todo

    # Importa e registra as rotas (endpoints)
    from . import routes
    app.register_blueprint(routes.api_bp)

    return app