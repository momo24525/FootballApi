import asyncio
from datetime import date, timedelta

from app.config import settings
from app.bigballs_client import BigBallsClient
from app.db import SessionLocal
from app.crud.team import get_or_create_team
from app.crud.season import get_or_create_season
from app.crud.match import get_match_by_teams_and_matchday, create_match
from app.schemas.match import MatchCreate


SEASON_YEAR = 2026
SEASON_START = date(2026, 8, 20)   # adatta alle date reali della stagione
SEASON_END = date(2026, 9, 8)


def map_api_match_to_create(data: dict, season_id: int, db) -> MatchCreate | None:
    if data["status"] != "finished":
        return None

    home_team = get_or_create_team(db, data["home"]["name"])
    away_team = get_or_create_team(db, data["away"]["name"])

    round_str = data.get("round")
    matchday = 1
    if round_str:
        try:
            matchday = int(round_str.split("-")[-1].strip())
        except (ValueError, AttributeError):
            matchday = 1

    from datetime import datetime
    match_date = datetime.fromisoformat(
        data["kickoff_utc"].replace("Z", "+00:00")
    ).date()

    return MatchCreate(
        matchday=matchday,  #type:ignore
        home_team_id=home_team.id, #type:ignore
        away_team_id=away_team.id, #type:ignore
        season_id=season_id,
        home_goals=data["score"]["home"],
        away_goals=data["score"]["away"],
        match_date=match_date,
    )


async def import_matches():
    client = BigBallsClient(settings)
    db = SessionLocal()

    imported = 0
    skipped = 0

    try:
        season = get_or_create_season(db, year=SEASON_YEAR)

        current_day = SEASON_START
        while current_day <= SEASON_END:
            day_str = current_day.isoformat()
            response = await client.list_serie_a_matches(status="finished", date=day_str, limit=20)
            if not isinstance(response.get("data"), list):
                print(f"  {day_str}: risposta inattesa -> {response}")
            
            matches_data = response.get("data", [])
            
            if not isinstance(matches_data, list):
                # giorno senza partite, o risposta in formato inatteso: salta
                current_day += timedelta(days=1)
                await asyncio.sleep(0.7)
                continue

            for data_item in matches_data:
                match_in = map_api_match_to_create(data_item, season.id, db)#type:ignore
                if match_in is None:
                    skipped += 1
                    continue

                existing = get_match_by_teams_and_matchday(
                    db, match_in.home_team_id, match_in.away_team_id,
                    match_in.season_id, match_in.matchday  #type:ignore
                )
                if existing:
                    skipped += 1
                    continue

                create_match(db, match_in)
                imported += 1
                print(f"  {day_str}: giornata {match_in.matchday} "
                      f"{data_item['home']['name']} {match_in.home_goals}-"
                      f"{match_in.away_goals} {data_item['away']['name']}")

            current_day += timedelta(days=1)
            await asyncio.sleep(0.7)  # piccola pausa per non martellare l'API

        print(f"\nFatto. Importate: {imported}, saltate: {skipped}")

    finally:
        db.close()
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(import_matches())