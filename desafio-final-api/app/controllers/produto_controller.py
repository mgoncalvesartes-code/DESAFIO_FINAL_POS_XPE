from flask import Blueprint, jsonify, request, url_for

from app.schemas.produto_schema import (
    serializar_lista,
    serializar_produto,
    validar_payload,
)
from app.services.produto_service import ProdutoService

produto_bp = Blueprint("produtos", __name__, url_prefix="/produtos")

service = ProdutoService()


@produto_bp.get("")
def listar_todos():
    produtos = service.listar_todos()
    return jsonify(serializar_lista(produtos)), 200


# /contar precisa vir antes de /<int:produto_id> (na verdade o conversor int
# já segura, mas deixo aqui em cima de propósito)
@produto_bp.get("/contar")
def contar():
    return jsonify({"total": service.contar()}), 200


@produto_bp.get("/nome/<string:nome>")
def buscar_por_nome(nome: str):
    produtos = service.buscar_por_nome(nome)
    return jsonify(serializar_lista(produtos)), 200


@produto_bp.get("/<int:produto_id>")
def buscar_por_id(produto_id: int):
    produto = service.buscar_por_id(produto_id)  # lança 404 se não existir
    return jsonify(serializar_produto(produto)), 200


@produto_bp.post("")
def criar():
    dados = validar_payload(request.get_json(silent=True) or {}, parcial=False)
    produto = service.criar(dados)
    local = url_for("produtos.buscar_por_id", produto_id=produto.id)
    return jsonify(serializar_produto(produto)), 201, {"Location": local}


@produto_bp.put("/<int:produto_id>")
def atualizar(produto_id: int):
    dados = validar_payload(request.get_json(silent=True) or {}, parcial=True)
    produto = service.atualizar(produto_id, dados)
    return jsonify(serializar_produto(produto)), 200


@produto_bp.delete("/<int:produto_id>")
def deletar(produto_id: int):
    service.deletar(produto_id)
    return "", 204
