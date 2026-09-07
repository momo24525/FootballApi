from app.db import engine, Base
from app import models  # importante: serve per "registrare" i modelli su Base

Base.metadata.create_all(bind=engine)

print("Database e tabelle creati con successo.")