from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, asc, desc
from app.models.match import Match
from app.models.team import Team
from app.models.season import Season
from app.schemas.match import MatchCreate
from fastapi import HTTPException

def get_match_by_teams_and_matchday(
    db: Session,
    home_team_id: int,
    away_team_id: int,
    season_id: int,
    matchday: int,
) -> Match | None:
    return db.query(Match).filter(
        Match.home_team_id == home_team_id,
        Match.away_team_id == away_team_id,
        Match.season_id == season_id,
        Match.matchday == matchday,
    ).first()




def create_match(db: Session, match_in: MatchCreate) -> Match:
    match = Match(**match_in.model_dump())
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def get_matches(
    db: Session,
    team_name: str | None = None,
    year: int | None = None,
    matchday: int | None = None,
    skip: int = 0,
    limit: int = 380,
) -> list[Match]:
    query = db.query(Match).join(Match.season)

    if year:
        query = query.filter(Match.season.has(year=year))

    if matchday:
        query = query.filter(Match.matchday == matchday)

        
    if team_name:
        query = query.filter(
            (Match.home_team.has(Team.name.ilike(team_name))) |
            (Match.away_team.has(Team.name.ilike(team_name)))
        )

    results = query.order_by(desc(Season.year), desc(Match.matchday)).offset(skip).limit(limit).all()
    
    if not results:
        detail = f"Nessun incontro trovato per {team_name}"
        if year:
            detail += f" nella stagione {year} - {year + 1}"

        raise HTTPException(status_code=404, detail=detail)

    return results

        
def get_head_to_head(
    db: Session, team1_name: str, team2_name: str, year: int | None = None, matchday: int | None = None
) -> list[Match]:
    query = db.query(Match).filter(
        or_(
            and_(
                Match.home_team.has(Team.name.ilike(team1_name)),
                Match.away_team.has(Team.name.ilike(team2_name)),
            ),
            and_(
                Match.home_team.has(Team.name.ilike(team2_name)),
                Match.away_team.has(Team.name.ilike(team1_name)),
            ),
        )
    )

    if year:
        query = query.filter(Match.season.has(year=year))
        
    if matchday:
        query = query.filter(Match.matchday == matchday)
        
    results = query.order_by(Match.match_date.desc()).all()
    
    if not results:
        detail = f"Nessun incontro trovato tra '{team1_name}' e '{team2_name}'"
        if year:
            detail += f" nella stagione {year} - {year + 1}"

        raise HTTPException(status_code=404, detail=detail)

    return results