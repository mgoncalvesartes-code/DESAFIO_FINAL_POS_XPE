"""Regras de negócio dos produtos. Fala com o Repository, não com o ORM."""

from app.errors.exceptions import RecursoNaoEncontradoError
from app.models.produto import Produto
from app.repositories.produto_repository import ProdutoRepository


class ProdutoService:
    def __init__(self, repository: ProdutoRepository | None = None):
        self.repository = repository or ProdutoRepository()

    def listar_todos(self) -> list[Produto]:
        return self.repository.listar_todos()

    def buscar_por_id(self, produto_id: int) -> Produto:
        produto = self.repository.buscar_por_id(produto_id)
        if produto is None:
            raise RecursoNaoEncontradoError(
                f"Produto com id {produto_id} não encontrado."
            )
        return produto

    def buscar_por_nome(self, nome: str) -> list[Produto]:
        return self.repository.buscar_por_nome(nome)

    def contar(self) -> int:
        return self.repository.contar()

    def criar(self, dados: dict) -> Produto:
        produto = Produto(
            nome=dados["nome"],
            descricao=dados.get("descricao"),
            preco=dados["preco"],
            quantidade_estoque=dados.get("quantidade_estoque", 0),
        )
        return self.repository.salvar(produto)

    def atualizar(self, produto_id: int, dados: dict) -> Produto:
        produto = self.buscar_por_id(produto_id)  # 404 se não achar
        for campo, valor in dados.items():
            setattr(produto, campo, valor)
        return self.repository.salvar(produto)

    def deletar(self, produto_id: int) -> None:
        produto = self.buscar_por_id(produto_id)
        self.repository.deletar(produto)
