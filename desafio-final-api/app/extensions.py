from flask_sqlalchemy import SQLAlchemy

# fica isolado aqui pra não dar import circular (models importam daqui,
# o create_app chama db.init_app)
db = SQLAlchemy()
