from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    matchday = Column(Integer, nullable=True, index=True)
    match_date = Column(Date, nullable=True)

    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)

    home_goals = Column(Integer, nullable=False)
    away_goals = Column(Integer, nullable=False)
    
    isplayed = Column(Boolean, nullable=True)

    # Relazioni verso Team: serve foreign_keys esplicito perché ci sono 2 FK verso la stessa tabella
    home_team = relationship(
        "Team", foreign_keys=[home_team_id], back_populates="home_matches"
    )
    away_team = relationship(
        "Team", foreign_keys=[away_team_id], back_populates="away_matches"
    )
    season = relationship("Season", back_populates="matches")
  
    __table_args__ = (  #Evita che ci siano due home/away team_id uguali, season_id e matchday nella stessa riga
        UniqueConstraint(
            "home_team_id", "away_team_id", "season_id", "matchday",
            name="uq_match_unique"
        ),
    )