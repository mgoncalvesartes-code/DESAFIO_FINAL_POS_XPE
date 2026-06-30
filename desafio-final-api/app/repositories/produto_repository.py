# Acesso ao banco. Tudo que toca o SQLAlchemy mora aqui — se um dia trocar
# o SQLite por outro banco, mexe só neste arquivo.

from app.extensions import db
from app.models.produto import Produto


class ProdutoRepository:

    def listar_todos(self) -> list[Produto]:
        stmt = db.select(Produto).order_by(Produto.id)
        return list(db.session.scalars(stmt).all())

    def buscar_por_id(self, produto_id: int) -> Produto | None:
        return db.session.get(Produto, produto_id)

    def buscar_por_nome(self, nome: str) -> list[Produto]:
        # % dos dois lados = "contém"; ilike ignora maiúscula/minúscula
        termo = f"%{nome}%"
        stmt = (
            db.select(Produto)
            .where(Produto.nome.ilike(termo))
            .order_by(Produto.nome)
        )
        return list(db.session.scalars(stmt).all())

    def contar(self) -> int:
        stmt = db.select(db.func.count()).select_from(Produto)
        return db.session.scalar(stmt)

    def salvar(self, produto: Produto) -> Produto:
        db.session.add(produto)
        db.session.commit()
        db.session.refresh(produto)
        return produto

    def deletar(self, produto: Produto) -> None:
        db.session.delete(produto)
        db.session.commit()
