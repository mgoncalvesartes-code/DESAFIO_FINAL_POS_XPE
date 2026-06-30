class APIError(Exception):
    """Erro base da aplicação."""

    status_code = 400
    mensagem = "Erro na requisição."

    def __init__(self, mensagem: str | None = None, status_code: int | None = None):
        super().__init__(mensagem or self.mensagem)
        if mensagem:
            self.mensagem = mensagem
        if status_code:
            self.status_code = status_code

    def to_dict(self) -> dict:
        return {"erro": self.mensagem, "status": self.status_code}


class RecursoNaoEncontradoError(APIError):
    """Recurso inexistente (HTTP 404)."""

    status_code = 404
    mensagem = "Recurso não encontrado."


class ValidacaoError(APIError):
    """Dados de entrada inválidos (HTTP 400)."""

    status_code = 400
    mensagem = "Dados inválidos."
