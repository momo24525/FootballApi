import re
import sys
from datetime import date

from app.db import SessionLocal
from app.crud.team import get_or_create_team
from app.crud.season import get_or_create_season
from app.crud.match import get_match_by_teams_and_matchday, create_match
from app.schemas.match import MatchCreate
from import_matches import (
    MONTHS, MATCHDAY_HEADER_RE, DATE_RE, HEADER_RE,
    MATCH_RE_A, MATCH_RE_B, FIXTURE_RE_A,
)


def parse_fixtures(filepath: str, season_start_year: int) -> list[dict]:
    """Restituisce solo le partite SENZA punteggio (future)."""
    fixtures = []
    current_matchday = None
    current_date = None

    with open(filepath, encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            stripped = line.strip()
            if not stripped or HEADER_RE.match(stripped):
                continue

            if MATCHDAY_HEADER_RE.search(stripped):
                num = re.search(r"(\d+)\s*$", stripped)
                if num:
                    current_matchday = int(num.group(1))
                continue

            dm = DATE_RE.match(stripped)
            if dm:
                month_str, day_str, year_str = dm.groups()
                month = MONTHS.get(month_str)
                if month is None:
                    continue
                year = int(year_str) if year_str else (
                    season_start_year if month >= 7 else season_start_year + 1
                )
                current_date = date(year, month, int(day_str))
                continue

            # ha un punteggio -> gia' giocata, non e' compito di questo script
            if MATCH_RE_A.match(line) or MATCH_RE_B.match(line):
                continue

            fm = FIXTURE_RE_A.match(line)
            if fm and current_matchday is not None and current_date is not None:
                fixtures.append({
                    "matchday": current_matchday,
                    "match_date": current_date,
                    "home": fm.group("home").strip(),
                    "away": fm.group("away").strip(),
                })

    return fixtures


def import_fixtures(filepath: str, season_start_year: int):
    db = SessionLocal()
    imported = 0
    skipped = 0

    try:
        season = get_or_create_season(db, year=season_start_year)
        fixtures = parse_fixtures(filepath, season_start_year)
        print(f"Trovate {len(fixtures)} partite future nel file.\n")

        for fx in fixtures:
            home_team = get_or_create_team(db, fx["home"])
            away_team = get_or_create_team(db, fx["away"])

            existing = get_match_by_teams_and_matchday(
                db, home_team.id, away_team.id, season.id, fx["matchday"]  # type: ignore
            )
            if existing:
                skipped += 1
                continue

            match_in = MatchCreate(
                matchday=fx["matchday"],
                home_team_id=home_team.id,  # type: ignore
                away_team_id=away_team.id,  # type: ignore
                season_id=season.id,  # type: ignore
                home_goals=0,
                away_goals=0,
                match_date=fx["match_date"],
                isplayed=False,
            )
            create_match(db, match_in)
            imported += 1
            print(f"  giornata {fx['matchday']}: {fx['home']} v {fx['away']} ({fx['match_date']})")

        print(f"\nFatto. Importate: {imported}, saltate: {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python import_fixtures.py <file.txt> <anno_inizio_stagione>")
        sys.exit(1)
    import_fixtures(sys.argv[1], int(sys.argv[2]))