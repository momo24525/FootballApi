from sqlalchemy.orm import Session

from app.models.team import Team
from app.schemas.team import TeamCreate


def get_team_by_name(db: Session, name: str) -> Team | None:
    return db.query(Team).filter(Team.name == name).first()


def get_or_create_team(db: Session, name: str, city: str | None = None) -> Team:
    team = get_team_by_name(db, name)
    if team:
        return team

    team = Team(name=name, city=city)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def get_teams(db: Session, skip: int = 0, limit: int = 100) -> list[Team]:
    return db.query(Team).offset(skip).limit(limit).all()