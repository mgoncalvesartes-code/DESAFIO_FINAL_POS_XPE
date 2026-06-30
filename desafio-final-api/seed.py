# roda com: python seed.py
# joga uns produtos no banco pra não começar vazio

from decimal import Decimal

from app import create_app
from app.extensions import db
from app.models.produto import Produto

PRODUTOS_EXEMPLO = [
    {"nome": "Notebook Pro 14", "descricao": "Notebook 14'' 16GB RAM", "preco": Decimal("6499.90"), "quantidade_estoque": 12},
    {"nome": "Mouse sem fio", "descricao": "Mouse óptico Bluetooth", "preco": Decimal("129.90"), "quantidade_estoque": 80},
    {"nome": "Teclado mecânico", "descricao": "Switch marrom, ABNT2", "preco": Decimal("349.00"), "quantidade_estoque": 35},
    {"nome": "Monitor 27 4K", "descricao": "Monitor IPS 27'' 4K", "preco": Decimal("2199.00"), "quantidade_estoque": 8},
    {"nome": "Webcam Full HD", "descricao": "Webcam 1080p com microfone", "preco": Decimal("259.90"), "quantidade_estoque": 50},
]


def run():
    app = create_app()
    with app.app_context():
        if db.session.scalar(db.select(db.func.count()).select_from(Produto)) > 0:
            print("Banco já contém produtos. Seed ignorado.")
            return
        for dados in PRODUTOS_EXEMPLO:
            db.session.add(Produto(**dados))
        db.session.commit()
        print(f"{len(PRODUTOS_EXEMPLO)} produtos inseridos com sucesso.")


if __name__ == "__main__":
    run()
