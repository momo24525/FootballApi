from sqlalchemy.orm import Session

from app.models.team import Team
from app.schemas.team import TeamCreate


def get_team_by_name(db: Session, name: str) -> Team | None:
    return db.query(Team).filter(Team.name == name).first()


TEAM_NAME_MAP = {   #risolve i problemi di naming
    "FC Internazionale Milano": "Internazionale",
    "Juventus FC": "Juventus",
    "Frosinone Calcio": "Frosinone",
    "US Lecce": "Lecce",
    "Atalanta BC": "Atalanta",
    "US Sassuolo Calcio": "Sassuolo",
    "Torino FC": "Torino",
    "Bologna FC 1909": "Bologna",
    "SS Lazio": "Lazio",
    "ACF Fiorentina": "Fiorentina",
    "AC Monza": "Monza",
    "Udinese Calcio": "Udinese",
    "Parma Calcio 1913": "Parma",
    "SSC Napoli": "Napoli",
    "Como 1907": "Como",
    "Genoa CFC": "Genoa",
    "Cagliari Calcio": "Cagliari",
    "AS Roma": "Roma",
    "AC Milan": "Milan",
    "Venezia FC": "Venezia",
    "Hellas Verona FC": "Hellas Verona",
    "Empoli FC": "Empoli",
    "US Salernitana 1919": "Salernitana",
    "Spezia Calcio": "Spezia",
    "UC Sampdoria": "Sampdoria",
    "Benevento Calcio": "Benevento",
    "FC Crotone": "Crotone",
    "Lazio Roma": "Lazio",
    "SPAL 2013 Ferrara": "Spal",
    "Brescia Calcio": "Brescia",
    "Bologna FC": "Bologna",  
    "Sassuolo Calcio": "Sassuolo",    
    "Inter": "Internazionale",
    "US Palermo": "Palermo",
    "Delfino Pescara": "Pescara",
    "Carpi FC": "Carpi",
    "Parma FC": "Parma",
    "AC Cesena": "Cesena",
    "AS Livorno": "Livorno",
    "Calcio Catania": "Catania"
}


def normalize_team_name(name: str) -> str:
    return TEAM_NAME_MAP.get(name, name)


def get_or_create_team(db: Session, name: str, city: str | None = None) -> Team:
    name = normalize_team_name(name)

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