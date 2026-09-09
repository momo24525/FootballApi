from datetime import date
from pydantic import BaseModel


class MatchCreate(BaseModel):
    matchday: int | None = None
    home_team_id: int
    away_team_id: int
    season_id: int
    home_goals: int
    away_goals: int
    match_date: date | None = None


class MatchOut(BaseModel):
    id: int
    matchday: int | None = None
    match_date: date | None = None
    home_goals: int
    away_goals: int
    home_team: str    # nome squadra, non id
    away_team: str
    season: int        # anno, non id

    class Config:
        from_attributes = True
