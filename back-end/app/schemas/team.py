from pydantic import BaseModel


class TeamCreate(BaseModel):
    name: str
    city: str | None = None


class TeamOut(BaseModel):
    id: int
    name: str
    city: str | None = None

    class Config:
        from_attributes = True  # permette di creare lo schema direttamente da un oggetto SQLAlchemy