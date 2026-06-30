"""Handlers globais: transformam as exceções em resposta JSON."""

from flask import jsonify

from app.errors.exceptions import APIError


def registrar_error_handlers(app):
    @app.errorhandler(APIError)
    def tratar_api_error(erro: APIError):
        return jsonify(erro.to_dict()), erro.status_code

    @app.errorhandler(404)
    def tratar_404(_):
        return jsonify({"erro": "Rota não encontrada.", "status": 404}), 404

    @app.errorhandler(405)
    def tratar_405(_):
        return jsonify({"erro": "Método não permitido.", "status": 405}), 405

    @app.errorhandler(500)
    def tratar_500(_):
        return jsonify({"erro": "Erro interno do servidor.", "status": 500}), 500
