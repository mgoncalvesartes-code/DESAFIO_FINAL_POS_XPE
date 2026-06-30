"""Fábrica da aplicação (create_app)."""

from flask import Flask, jsonify

from app.config import config_by_name
from app.errors import registrar_error_handlers
from app.extensions import db


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__)
    # Fallback usa a CLASSE de configuração padrão (não a string), evitando que
    # um config_name inválido seja interpretado como caminho de import.
    app.config.from_object(
        config_by_name.get(config_name, config_by_name["development"])
    )

    # Extensões
    db.init_app(app)

    # Blueprints (Controllers)
    from app.controllers import produto_bp

    app.register_blueprint(produto_bp)

    # Handlers de erro globais
    registrar_error_handlers(app)

    # Rota raiz: pequena "documentação viva" da API.
    @app.get("/")
    def index():
        return jsonify(
            {
                "api": "Desafio Final - Arquiteto de Software",
                "dominio": "Produto",
                "padrao": "MVC (Controller / Service / Repository / Model + View)",
                "endpoints": {
                    "GET    /produtos": "Find All - lista todos os produtos",
                    "GET    /produtos/<id>": "Find By ID - busca por ID",
                    "GET    /produtos/nome/<nome>": "Find By Name - busca por nome",
                    "GET    /produtos/contar": "Count - total de registros",
                    "POST   /produtos": "Create - cria um produto",
                    "PUT    /produtos/<id>": "Update - atualiza um produto",
                    "DELETE /produtos/<id>": "Delete - remove um produto",
                },
            }
        )

    # Cria as tabelas no primeiro start (idempotente).
    with app.app_context():
        db.create_all()

    return app
