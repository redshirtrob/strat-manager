from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, Integer, String

from blb.models.core import Base

class Team(Base):
    """MLB Teams"""
    __tablename__ = 'fg_team'

    id = Column(Integer, primary_key=True)
    location = Column(String(30))
    nickname = Column(String(30))
    abbreviation = Column(String(4))

    # many to many Team<->FGPlayerSeason
#    player_seasons = relationship('FGPlayerSeason',
#                                  secondary=player_seasons_teams,
#                                  back_populates='mlb_teams')


class Season(Base):
    """A single season"""
    __tablename__ = 'fg_season'

    id = Column(Integer, primary_key=True)
    year = Column(String(4))
    
    
class Player(Base):
    """Players in the Fangraphs database"""
    __tablename__ = 'fg_player'

    id = Column(Integer, primary_key=True)
    last_name = Column(String(30))
    first_name = Column(String(30))


#player_season_teams = Table('player_season_teams', Base.metadata,
#                            Column('player_season_id', ForeignKey('fg_player_season.id'), primary_key=True),
#                            Column('mlb_team_id', ForeignKey('mlb_team.id'), primary_key=True))


class PlayerSeason(Base):
    """Relate player/season to teams"""
    __tablename__ = 'fg_player_season'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('fg_player.id'))
    season_id = Column(Integer, ForeignKey('fg_season.id'))

    # many to many PlayerSeason<->MLBTeam
#    teams = relationship('MLBTeam',
#                         secondary=player_season_teams,
#                         back_populates='fg_player_seasons')

    
# "Name","Team","G","PA","HR","R","RBI","SB","BB%","K%","ISO","BABIP","AVG","OBP","SLG",
# "wOBA","wRC+","BsR","Off","Def","WAR","AB","H","1B","2B","3B","BB","IBB","SO","HBP","GDP",
# "CS","GB","FB","LD","IFFB","playerid"
class Batting(Base):
    """Batting statistics for a single MLB season"""
    __tablename__ = 'fg_batting'

    id = Column(Integer, primary_key=True)
    player_season_id = Column(Integer, ForeignKey('fg_player_season.id'))

    g = Column(Integer)
    pa = Column(Integer)
    hr = Column(Integer)
    r = Column(Integer)
    rbi = Column(Integer)
    sb = Column(Integer)
    bb_pct = Column(Float)
    k_pct = Column(Float)
    iso = Column(Float)
    babip = Column(Float)
    avg = Column(Float)
    obp = Column(Float)
    slg = Column(Float)
    woba = Column(Float)
    wrc_plus = Column(Integer)
    bsr = Column(Float)
    off = Column(Float)
    defense = Column(Float)
    war = Column(Float)
    ab = Column(Integer)
    h = Column(Integer)
    single = Column(Integer)
    double = Column(Integer)
    triple = Column(Integer)
    bb = Column(Integer)
    ibb = Column(Integer)
    so = Column(Integer)
    hbp = Column(Integer)
    gdp = Column(Integer)
    cs = Column(Integer)
    gb = Column(Integer)
    fb = Column(Integer)
    ld = Column(Integer)
    iffb = Column(Integer)
    
    
# "Name","Team","W","L","SV","G","GS","IP","K/9","BB/9","HR/9","BABIP","LOB%","GB%","HR/FB",
# "ERA","FIP","xFIP","WAR","CG","H","R","ER","HR","BB","IBB","HBP","WP","BK","SO","GB","FB",
# "LD","playerid"
class Pitching(Base):
    """Pitching statistics for a single MLB season"""
    __tablename__ = 'fg_pitching'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('fg_player.id'))
    season_id = Column(Integer, ForeignKey('fg_season.id'))
