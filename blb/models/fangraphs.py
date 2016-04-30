from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, Integer, String

from blb.models.core import Base

fg_player_season_teams = Table('fg_player_season_teams', Base.metadata,
                               Column('player_season_id', ForeignKey('fg_player_season.id'), primary_key=True),
                               Column('fg_team_id', ForeignKey('fg_team.id'), primary_key=True))

class FGTeam(Base):
    """MLB Teams"""
    __tablename__ = 'fg_team'

    id = Column(Integer, primary_key=True)
    location = Column(String(30))
    nickname = Column(String(30))
    abbreviation = Column(String(4))

    # many to many FGTeam<->FGPlayerSeason
    player_seasons = relationship('FGPlayerSeason',
                                  secondary=fg_player_season_teams,
                                  back_populates='teams')

    def __repr__(self):
        return "<FGTeam({} {})>".format(self.location, self.nickname)


class FGSeason(Base):
    """A single season"""
    __tablename__ = 'fg_season'

    id = Column(Integer, primary_key=True)
    year = Column(String(4))

    player_seasons = relationship("FGPlayerSeason")

    def __repr__(self):
        return "<FGSeason({})>".format(self.year)

    
class FGPlayer(Base):
    """Players in the Fangraphs database"""
    __tablename__ = 'fg_player'

    id = Column(Integer, primary_key=True)
    last_name = Column(String(30))
    first_name = Column(String(30))

    player_seasons = relationship("FGPlayerSeason")

    def __repr__(self):
        return "<FGPlayer({})>".format(self.fullname)

    @property
    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)
        

class FGPlayerSeason(Base):
    """Relate player/season/team/stats
    
    This model creates a relationship between a FGPlayer and FGSeason
    model with the teams and statistics models for that player and
    that season.
    """
    __tablename__ = 'fg_player_season'

    id = Column(Integer, primary_key=True)

    # Basic FGPlayer data
    player_id = Column(Integer, ForeignKey('fg_player.id'))
    player = relationship("FGPlayer", uselist=False)

    # Basic FGSeason data
    season_id = Column(Integer, ForeignKey('fg_season.id'))
    season = relationship("FGSeason", back_populates="player_seasons", uselist=False)

    # Teams the player played for during the season
    teams = relationship('FGTeam',
                         secondary=fg_player_season_teams,
                         back_populates='player_seasons')

    # FGBatting statistics for the season
    batting = relationship('FGBatting', back_populates="player_season", uselist=False)

    # FGPitching statistics for the season
    pitching = relationship('FGPitching', back_populates="player_season", uselist=False)

    def __repr__(self):
        return "<FGPlayerSeason(FGPlayer={}, FGSeason={})>".format(
            self.player.fullname,
            self.season.year
        )

    
# "Name","FGTeam","G","PA","HR","R","RBI","SB","BB%","K%","ISO","BABIP","AVG","OBP","SLG",
# "wOBA","wRC+","BsR","Off","Def","WAR","AB","H","1B","2B","3B","BB","IBB","SO","HBP","GDP",
# "CS","GB","FB","LD","IFFB","playerid"
class FGBatting(Base):
    """FGBatting statistics for a single MLB season"""
    __tablename__ = 'fg_batting'

    id = Column(Integer, primary_key=True)
    player_season_id = Column(Integer, ForeignKey('fg_player_season.id'))
    player_season = relationship("FGPlayerSeason", back_populates="batting", uselist=False)

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

    def __repr__(self):
        return "<FGBatting(FGPlayer={}, FGSeason={})>".format(
            self.player_season.player.fullname,
            self.player_season.season.year
        )

    def to_dict(self):
        dct = super(FGBatting, self).to_dict()
        dct['player_id'] = self.player_season.player.id
        dct['last_name'] = self.player_season.player.last_name
        dct['first_name'] = self.player_season.player.first_name
        dct['season'] = self.player_season.season.year
        return dct
    
# "Name","FGTeam","W","L","SV","G","GS","IP","K/9","BB/9","HR/9","BABIP","LOB%","GB%","HR/FB",
# "ERA","FIP","xFIP","WAR","CG","H","R","ER","HR","BB","IBB","HBP","WP","BK","SO","GB","FB",
# "LD","playerid"
class FGPitching(Base):
    """FGPitching statistics for a single MLB season"""
    __tablename__ = 'fg_pitching'

    id = Column(Integer, primary_key=True)
    player_season_id = Column(Integer, ForeignKey('fg_player_season.id'))
    player_season = relationship("FGPlayerSeason", back_populates="pitching", uselist=False)

    w = Column(Integer)
    l = Column(Integer)
    sv = Column(Integer)
    g = Column(Integer)
    gs = Column(Integer)
    ip = Column(Float)
    k_per_9 = Column(Float)
    bb_per_9 = Column(Float)
    hr_per_9 = Column(Float)
    babip = Column(Float)
    lob_pct = Column(Float)
    gb_pct = Column(Float)
    hr_per_fb = Column(Float)
    era = Column(Float)
    fip = Column(Float)
    xfip = Column(Float)
    war = Column(Float)
    cg = Column(Integer)
    h = Column(Integer)
    r = Column(Integer)
    er = Column(Integer)
    hr = Column(Integer)
    bb = Column(Integer)
    ibb = Column(Integer)
    hbp = Column(Integer)
    wp = Column(Integer)
    bk = Column(Integer)
    so = Column(Integer)
    gb = Column(Integer)
    fb = Column(Integer)
    ld = Column(Integer)

    def __repr__(self):
        return "<FGPitching(FGPlayer={}, FGSeason={})>".format(
            self.player_season.player.fullname,
            self.player_season.season.year
        )
    
    def to_dict(self):
        dct = super(FGPitching, self).to_dict()
        dct['player_id'] = self.player_season.player.id
        dct['last_name'] = self.player_season.player.last_name
        dct['first_name'] = self.player_season.player.first_name
        dct['season'] = self.player_season.season.year
        return dct
