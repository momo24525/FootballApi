from typing import Any

import httpx
from fastapi import HTTPException

from app.config import Settings


class BigBallsAPIError(Exception):
    """Raised when the upstream API returns a non-2xx response."""

    def __init__(self, status_code: int, payload: dict[str, Any]):
        self.status_code = status_code
        self.payload = payload
        super().__init__(f"Big Balls API error {status_code}: {payload}")


class BigBallsClient:
    """
    Thin async wrapper around api.bigballsdata.com.

    One instance is created at app startup and reused for every request
    (see main.py lifespan) so the underlying HTTP connection pool is shared.
    """

    def __init__(self, settings: Settings):
        self._settings = settings
        self._client = httpx.AsyncClient(
            base_url=settings.bigballs_base_url,
            headers={"Authorization": f"Bearer {settings.bigballs_api_key}"},
            timeout=settings.request_timeout_seconds,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            response = await self._client.get(path, params=params)
        except httpx.TimeoutException as exc:
            raise HTTPException(status_code=504, detail="Upstream API timed out") from exc
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"Upstream request failed: {exc}") from exc

        if response.status_code >= 400:
            # The API returns structured errors, often with a suggested_fix.
            # Surface that instead of a bare status code so callers can act on it.
            try:
                payload = response.json()
            except ValueError:
                payload = {"error": response.text}
            raise BigBallsAPIError(response.status_code, payload)

        return response.json()

    # --- Account / meta -------------------------------------------------

    async def whoami(self) -> dict[str, Any]:
        """GET /v1/user/me - confirms the key works and returns rate limits."""
        return await self._get("/v1/user/me")

    # --- Serie A specific helpers ----------------------------------------
    
    
    async def list_serie_a_matches(
        self, status: str | None = None, limit: int = 50, date: str | None = None
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"sport": "football", "league": "seriea", "limit": limit}
        if status:
            params["status"] = status
        if date:
            params["date"] = date
        return await self._get("/v1/matches", params=params)

    async def get_match(self, match_id: str, fields: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if fields:
            # e.g. "scores,odds,lineups,stats,events" forces the live envelope
            params["sport"] = "football"
            params["fields"] = fields
        return await self._get(f"/v1/matches/{match_id}", params=params)

    async def get_match_statistics(self, match_id: str) -> dict[str, Any]:
        return await self._get(f"/v1/matches/{match_id}/statistics")

    async def get_serie_a_standings(self) -> dict[str, Any]:
        return await self._get("/v1/standings", params={"league": "seriea"})

    async def get_serie_a_top_scorers(self, season: int) -> dict[str, Any]:
        return await self._get(
            "/v1/leagues/serie-a/top-scorers", params={"season": season}
        )

    async def get_serie_a_xg_leaders(self, stat: str = "xg") -> dict[str, Any]:
        return await self._get(
            "/v1/leagues/serie-a/xg-leaders", params={"stat": stat}
        )