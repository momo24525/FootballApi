from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=list[schemas.TeamOut])
def list_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_teams(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.TeamOut)
def create_team(team_in: schemas.TeamCreate, db: Session = Depends(get_db)):
    existing = crud.get_team_by_name(db, team_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="Team già esistente")
    return crud.get_or_create_team(db, name=team_in.name, city=team_in.city)