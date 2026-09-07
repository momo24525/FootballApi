from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import team, match, season

app = FastAPI(title="Calcio DB API")

app.include_router(team.router)
app.include_router(match.router)
app.include_router(season.router)


@app.get("/")
def root():
    return {"message": "Calcio DB API attiva. Vai su /docs per la documentazione."}



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_methods=["*"],
    allow_headers=["*"],
)