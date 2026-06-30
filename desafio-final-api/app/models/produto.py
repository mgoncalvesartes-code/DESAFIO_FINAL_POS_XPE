from datetime import datetime, timezone

from app.extensions import db


class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(120), nullable=False, index=True)
    descricao = db.Column(db.String(500), nullable=True)
    preco = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    quantidade_estoque = db.Column(db.Integer, nullable=False, default=0)
    data_criacao = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<Produto id={self.id} nome={self.nome!r}>"
