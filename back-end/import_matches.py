import re
import sys
from datetime import date
from app.db import SessionLocal
from app.crud.team import get_or_create_team
from app.crud.season import get_or_create_season
from app.crud.match import get_match_by_teams_and_matchday, create_match
from app.schemas.match import MatchCreate

MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}

MATCHDAY_HEADER_RE = re.compile(r"(Regular Season|Matchday)", re.IGNORECASE)
DATE_RE = re.compile(r"^[A-Za-z]{3}\s+([A-Za-z]{3})\s+(\d{1,2})(?:\s+(\d{4}))?\s*$")
HEADER_RE = re.compile(r"^[=#]")

# Formato A: "Home v Away  1-2 (0-1)" (con "v" letterale)
MATCH_RE_A = re.compile(
    r"^(?:\s*\d{1,2}:\d{2})?\s*"
    r"(?P<home>.+?)\s+v\s+(?P<away>.+?)\s+"
    r"(?P<hg>\d+)-(?P<ag>\d+)"
    r"(?:\s*\(\d+-\d+\))?"
    r"(?:\s*\[[^\]]*\])?\s*$"
)
FIXTURE_RE_A = re.compile(
    r"^(?:\s*\d{1,2}:\d{2})?\s*"
    r"(?P<home>.+?)\s+v\s+(?P<away>.+?)\s*$"
)

# Formato B: "Home  1-2 (0-1)  Away" (punteggio in mezzo, senza "v")
# Il parziale primo tempo tra parentesi e' OPZIONALE: alcune fonti non lo riportano
# Alcune righe hanno anche un'annotazione finale tipo "[awarded]" (partita a tavolino) - va scartata
MATCH_RE_B = re.compile(
    r"^(?:\s*\d{1,2}:\d{2})?\s*"
    r"(?P<home>.+?)\s+"
    r"(?P<hg>\d+)-(?P<ag>\d+)(?:\s*\(\d+-\d+\))?\s+"
    r"(?P<away>.+?)"
    r"(?:\s*\[[^\]]*\])?\s*$"
)


def parse_txt(filepath: str, season_start_year: int) -> list[dict]:
    """
    Legge il file e restituisce una lista di dict:
    {matchday, match_date, home, away, home_goals, away_goals}
    """
    results = []
    not_played = 0
    current_matchday = None
    current_date = None

    with open(filepath, encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            stripped = line.strip()
            if not stripped:
                continue

            if HEADER_RE.match(stripped):
                continue  # riga di metadati (=, #), non e' una partita

            if MATCHDAY_HEADER_RE.search(stripped):
                num_match = re.search(r"(\d+)\s*$", stripped)
                if num_match:
                    current_matchday = int(num_match.group(1))
                else:
                    print(f"⚠️  Impossibile leggere il numero di giornata da: '{stripped}'")
                continue

            date_match = DATE_RE.match(stripped)
            if date_match:
                month_str, day_str, year_str = date_match.groups()
                month = MONTHS.get(month_str)
                if month is None:
                    print(f"⚠️  Mese non riconosciuto: '{stripped}'")
                    continue
                if year_str:
                    year = int(year_str)  # anno esplicito nel file: usalo direttamente
                else:
                    # nessun anno nel file: deduci dal mese
                    year = season_start_year if month >= 7 else season_start_year + 1
                current_date = date(year, month, int(day_str))
                continue

            m = MATCH_RE_A.match(line) or MATCH_RE_B.match(line)
            if m and current_matchday is not None and current_date is not None:
                results.append({
                    "matchday": current_matchday,
                    "match_date": current_date,
                    "home": m.group("home").strip(),
                    "away": m.group("away").strip(),
                    "home_goals": int(m.group("hg")),
                    "away_goals": int(m.group("ag")),
                })
                continue

            # niente punteggio: partita non ancora giocata, saltata di proposito
            f = FIXTURE_RE_A.match(line)
            if f and current_matchday is not None and current_date is not None:
                not_played += 1
                continue

            print(f"⚠️  Riga non riconosciuta, ignorata: '{line}'")

    if not_played:
        print(f"ℹ️  {not_played} partite non ancora giocate, saltate (nessun punteggio).")

    return results


def import_from_txt(filepath: str, season_start_year: int):
    db = SessionLocal()
    imported = 0
    skipped = 0

    try:
        season = get_or_create_season(db, year=season_start_year)
        parsed = parse_txt(filepath, season_start_year)
        print(f"Trovate {len(parsed)} partite nel file.\n")

        for pm in parsed:
            home_team = get_or_create_team(db, pm["home"])
            away_team = get_or_create_team(db, pm["away"])

            existing = get_match_by_teams_and_matchday(
                db, home_team.id, away_team.id, season.id, pm["matchday"] #type:ignore
            )
            if existing:
                skipped += 1
                continue

            match_in = MatchCreate(
                matchday=pm["matchday"],
                home_team_id=home_team.id,  # type: ignore
                away_team_id=away_team.id,  # type: ignore
                season_id=season.id,  # type: ignore
                home_goals=pm["home_goals"],
                away_goals=pm["away_goals"],
                match_date=pm["match_date"],
            )
            create_match(db, match_in)
            imported += 1
            print(f"  giornata {pm['matchday']}: {pm['home']} {pm['home_goals']}-"
                  f"{pm['away_goals']} {pm['away']}")

        print(f"\nFatto. Importate: {imported}, saltate: {skipped}")

    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python import_from_txt.py <file.txt> <anno_inizio_stagione>")
        print("Esempio: python import_from_txt.py serieA_2016_17.txt 2016")
        sys.exit(1)

    filepath = sys.argv[1]
    season_start_year = int(sys.argv[2])
    import_from_txt(filepath, season_start_year)