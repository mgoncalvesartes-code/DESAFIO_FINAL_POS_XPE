# testes dos endpoints (test client do Flask + sqlite em memoria)
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402


class ProdutoAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def _criar(self, nome="Produto Teste", preco=10.0):
        return self.client.post(
            "/produtos", json={"nome": nome, "preco": preco, "quantidade_estoque": 3}
        )

    def test_create_retorna_201(self):
        resp = self._criar()
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.get_json()["nome"], "Produto Teste")

    def test_find_all(self):
        self._criar("A")
        self._criar("B")
        resp = self.client.get("/produtos")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), 2)

    def test_count(self):
        self._criar()
        resp = self.client.get("/produtos/contar")
        self.assertEqual(resp.get_json()["total"], 1)

    def test_find_by_id(self):
        pid = self._criar().get_json()["id"]
        resp = self.client.get(f"/produtos/{pid}")
        self.assertEqual(resp.status_code, 200)

    def test_find_by_id_inexistente_404(self):
        resp = self.client.get("/produtos/999")
        self.assertEqual(resp.status_code, 404)

    def test_find_by_name_parcial(self):
        self._criar("Teclado Mecânico")
        resp = self.client.get("/produtos/nome/teclado")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), 1)

    def test_update(self):
        pid = self._criar().get_json()["id"]
        resp = self.client.put(f"/produtos/{pid}", json={"preco": 99.9})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["preco"], 99.9)

    def test_delete_retorna_204(self):
        pid = self._criar().get_json()["id"]
        resp = self.client.delete(f"/produtos/{pid}")
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(self.client.get(f"/produtos/{pid}").status_code, 404)

    def test_create_sem_nome_400(self):
        resp = self.client.post("/produtos", json={"preco": 10})
        self.assertEqual(resp.status_code, 400)

    def test_create_preco_negativo_400(self):
        resp = self.client.post("/produtos", json={"nome": "X", "preco": -1})
        self.assertEqual(resp.status_code, 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)
