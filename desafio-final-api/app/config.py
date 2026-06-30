import os

# Diretório raiz do projeto (…/desafio-final-api)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Config:
    """Configuração base, comum a todos os ambientes."""

    # Persistência em arquivo SQLite (os dados sobrevivem a reinícios).
    # Pode ser sobrescrito pela variável de ambiente DATABASE_URL
    # (ex.: PostgreSQL em produção: postgresql://user:pass@host/db).
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'produtos.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    # Banco em memória para os testes não tocarem o arquivo real.
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False


# Mapeia o nome do ambiente para a classe de configuração.
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
