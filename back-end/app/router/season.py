from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import crud, schemas

router = APIRouter(prefix="/seasons", tags=["seasons"])


@router.get("/", response_model=list[schemas.SeasonOut])
def list_seasons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_seasons(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.SeasonOut)
def create_season(season_in: schemas.SeasonCreate, db: Session = Depends(get_db)):
    existing = crud.get_season_by_year(db, season_in.year)
    if existing:
        raise HTTPException(status_code=400, detail="Season già esistente")
    return crud.get_or_create_season(db, year=season_in.year)