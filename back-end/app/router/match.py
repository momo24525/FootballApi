from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import crud, schemas

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/", response_model=list[schemas.MatchOut])
def list_matches(
    team: str | None = None,
    year: int | None = None,
    matchday: int | None = None,
    skip: int = 0,
    limit: int = 380,
    db: Session = Depends(get_db),
):
    matches = crud.get_matches(
        db, team_name=team, year=year, matchday=matchday, skip=skip, limit=limit
    )
    return [
        schemas.MatchOut(
            id=m.id,  #type:ignore
            matchday=m.matchday,#type:ignore
            match_date=m.match_date,#type:ignore
            home_goals=m.home_goals,#type:ignore
            away_goals=m.away_goals,#type:ignore
            home_team=m.home_team.name,
            away_team=m.away_team.name,
            season=m.season.year,
        )
        for m in matches
    ]
    
@router.get("/fixtures", response_model=list[schemas.MatchOut])
def list_fixtures(
    team: str | None = None,
    year: int | None = None,
    matchday: int | None = None,
    skip: int = 0,
    limit: int = 380,
    db: Session = Depends(get_db),
):
    matches = crud.get_fixtures(
    db, team_name=team, matchday=matchday,year=year, skip=skip, limit=limit
)
    return [
        schemas.MatchOut(
            id=m.id,  #type:ignore
            matchday=m.matchday,#type:ignore
            match_date=m.match_date,#type:ignore
            home_goals= None,#type:ignore
            away_goals= None,#type:ignore
            home_team=m.home_team.name,
            away_team=m.away_team.name,
            season=m.season.year,
        )
        for m in matches
    ]
    

    
@router.get("/headtohead", response_model=list[schemas.MatchOut])
def list_h2h(
    team1: str, 
    team2: str,
    year: int | None = None,
    matchday: int | None = None,
    db: Session = Depends(get_db),
):
    matches = crud.get_head_to_head(
        db, team1_name=team1, team2_name=team2, year=year, matchday=matchday
    )
    return [
        schemas.MatchOut(
            id=m.id,  #type:ignore
            matchday=m.matchday,#type:ignore
            match_date=m.match_date,#type:ignore
            home_goals=m.home_goals if m.isplayed else None,  # type: ignore
            away_goals=m.away_goals if m.isplayed else None,  # type: ignore
            home_team=m.home_team.name,
            away_team=m.away_team.name,
            season=m.season.year,
        )
        for m in matches
    ]
    
@router.post("/", response_model=schemas.MatchOut)
def create_match(match_in: schemas.MatchCreate, db: Session = Depends(get_db)):
    existing = crud.get_match_by_teams_and_matchday(
        db, match_in.home_team_id, match_in.away_team_id,
        match_in.season_id, match_in.matchday #type:ignore
    )
    if existing:
        raise HTTPException(status_code=400, detail="Partita già esistente")

    match = crud.create_match(db, match_in)

    return schemas.MatchOut(
        id=match.id, #type:ignore
        matchday=match.matchday, #type:ignore
        match_date=match.match_date, #type:ignore
        home_goals=match.home_goals, #type:ignore
        away_goals=match.away_goals, #type:ignore
        home_team=match.home_team.name,
        away_team=match.away_team.name,
        season=match.season.year,
    )