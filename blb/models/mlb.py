from sqlalchemy import Column, Integer, String

from blb.models.core import Base
#from blb.models.fangraphs import player_season_teams
#from blb.models.fangraphs import PlayerSeason as FGPlayerSeason

class Team(Base):
    """MLB Teams"""
    __tablename__ = 'mlb_team'

    id = Column(Integer, primary_key=True)
    location = Column(String(30))
    nickname = Column(String(30))
    abbreviation = Column(String(4))

    # many to many Team<->FGPlayerSeason
#    player_seasons = relationship('FGPlayerSeason',
#                                  secondary=player_seasons_teams,
#                                  back_populates='mlb_teams')
