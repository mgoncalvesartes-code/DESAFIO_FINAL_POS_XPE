# Serialização (Produto -> dict pra JSON) e validação do payload de entrada.
# Aqui é o "V" do MVC numa API: a View é o JSON, não uma tela.

from decimal import Decimal, InvalidOperation

from app.errors.exceptions import ValidacaoError


def serializar_produto(produto) -> dict:
    """Produto -> dict pronto pro jsonify."""
    return {
        "id": produto.id,
        "nome": produto.nome,
        "descricao": produto.descricao,
        "preco": float(produto.preco) if produto.preco is not None else None,
        "quantidade_estoque": produto.quantidade_estoque,
        "data_criacao": (
            produto.data_criacao.isoformat() if produto.data_criacao else None
        ),
    }


def serializar_lista(produtos) -> list:
    return [serializar_produto(p) for p in produtos]


def validar_payload(dados: dict, parcial: bool = False) -> dict:
    """Valida o corpo do POST/PUT. parcial=True (update) deixa campos faltarem."""
    if not isinstance(dados, dict):
        raise ValidacaoError("O corpo da requisição deve ser um objeto JSON.")

    resultado = {}

    if "nome" in dados:
        nome = dados["nome"]
        if not isinstance(nome, str) or not nome.strip():
            raise ValidacaoError("O campo 'nome' deve ser um texto não vazio.")
        resultado["nome"] = nome.strip()
    elif not parcial:
        raise ValidacaoError("O campo 'nome' é obrigatório.")

    if "descricao" in dados:
        descricao = dados["descricao"]
        if descricao is not None and not isinstance(descricao, str):
            raise ValidacaoError("O campo 'descricao' deve ser um texto.")
        resultado["descricao"] = descricao.strip() if descricao else None

    if "preco" in dados:
        try:
            preco = Decimal(str(dados["preco"]))
        except (InvalidOperation, TypeError):
            raise ValidacaoError("O campo 'preco' deve ser um número.")
        if preco < 0:
            raise ValidacaoError("O campo 'preco' não pode ser negativo.")
        resultado["preco"] = preco
    elif not parcial:
        raise ValidacaoError("O campo 'preco' é obrigatório.")

    if "quantidade_estoque" in dados:
        qtd = dados["quantidade_estoque"]
        # bool é subclasse de int, então True/False passariam — barro aqui
        if not isinstance(qtd, int) or isinstance(qtd, bool) or qtd < 0:
            raise ValidacaoError(
                "O campo 'quantidade_estoque' deve ser um inteiro >= 0."
            )
        resultado["quantidade_estoque"] = qtd

    if not resultado:
        raise ValidacaoError("Nenhum campo válido foi informado.")

    return resultado
