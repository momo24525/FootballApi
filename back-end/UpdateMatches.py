from datetime import date
from sqlalchemy import update
from app.db import SessionLocal
from app.models.match import Match  


def mark_played_matches():
    db = SessionLocal()
    try:
        today = date.today()
        result = db.execute(
            update(Match)
            .where(Match.match_date < today, Match.isplayed.is_(False))
            .values(isplayed=True)
        )
        db.commit()
        print(f"Aggiornate {result.rowcount} partite (match_date < {today}).") 
    finally:
        db.close()


if __name__ == "__main__":
    mark_played_matches()