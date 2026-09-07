from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Connection string per SQLite: crea il file calcio.db nella root del progetto
SQLALCHEMY_DATABASE_URL = "sqlite:///./calcio.db"

# connect_args è necessario SOLO per SQLite (per usarlo con più thread, tipo FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Fabbrica di sessioni: ogni richiesta HTTP ne aprirà una
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base da cui erediteranno tutti i modelli ORM (models.py)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()