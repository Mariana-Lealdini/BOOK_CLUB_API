from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Importa os modelos para registrá-los no metadata do SQLAlchemy
# antes da criação automática das tabelas.
from model.base import Base
from model.books import Book    # noqa: F401
from model.member import Member # noqa: F401
from model.rating import Rating # noqa: F401

db_path = "database/"

if not os.path.exists(db_path):
    os.makedirs(db_path)

db_url = f"sqlite:///{db_path}/db.sqlite3"

engine = create_engine(db_url, echo=False)
Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)