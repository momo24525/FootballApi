from sqlalchemy.orm import Session

from app.models.season import Season


def get_season_by_year(db: Session, year: int) -> Season | None:
    return db.query(Season).filter(Season.year == year).first()


def get_or_create_season(db: Session, year: int) -> Season:
    season = get_season_by_year(db, year)
    if season:
        return season

    season = Season(year=year)
    db.add(season)
    db.commit()
    db.refresh(season)
    return season


def get_seasons(db: Session, skip: int = 0, limit: int = 100) -> list[Season]:
    return db.query(Season).offset(skip).limit(limit).all()