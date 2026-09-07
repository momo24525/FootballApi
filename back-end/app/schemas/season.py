from pydantic import BaseModel


class SeasonCreate(BaseModel):
    year: int


class SeasonOut(BaseModel):
    id: int
    year: int

    class Config:
        from_attributes = True