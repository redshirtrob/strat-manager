from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, Integer, String

from .core import Base
from .fangraphs import FGPlayer

class BLBLeague(Base):
    """BLB Leagues"""
    __tablename__ = 'blb_league'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    abbreviation = Column(String(10))

    # Many BLBSeasons to One BLBLeague
    seasons = relationship('BLBSeason', back_populates='league')

    def __repr__(self):
        return "<BLBLeague({} {})>".format(self.name, self.abbreviation)

    def to_dict(self):
        dct = super(BLBLeague, self).to_dict()
        dct['name'] = self.name
        dct['abbreviation'] = self.abbreviation
        dct['seasons'] = [season.to_dict() for season in self.seasons]
        return dct


class BLBSeason(Base):
    """BLB Seasons"""
    __tablename__ = 'blb_season'

    id = Column(Integer, primary_key=True)
    year = Column(String(4))
    name = Column(String(50), nullable=True)

    # One BLBLeague to Many BLBSeasons
    league_id = Column(Integer, ForeignKey('blb_league.id'))
    league = relationship('BLBLeague', back_populates='seasons')

    # Many BLBDivisions to One BLBSeason
    divisions = relationship('BLBDivision', back_populates='season')

    # Many BLBTeams to One BLBSeason
    teams = relationship('BLBTeam', back_populates='season')

    def __repr__(self):
        if self.name is not None:
            return "<BLBSeason({} {})>".format(self.year, self.name)
        else:
            return "<BLBSeason({})>".format(self.year)

    @classmethod
    def from_dict(cls, dct):
        return cls(year=dct['year'], name=dct['name'], league_id=dct['league_id'])
    
    def to_dict(self):
        dct = super(BLBSeason, self).to_dict()
        dct['year'] = self.year
        dct['name'] = self.name
        return dct
        

class BLBDivision(Base):
    """BLB Divisions"""
    __tablename__ = 'blb_division'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    # One BLBSeason to Many BLBDivisions
    season_id = Column(Integer, ForeignKey('blb_season.id'))
    season = relationship('BLBSeason', back_populates='divisions')

    # Many BLBTeams to One BLBDivision
    teams = relationship('BLBTeam', back_populates='division')

    def __repr__(self):
        return "<BLBDivision({})>".format(self.name)

    @classmethod
    def from_dict(cls, dct):
        return cls(name=dct['name'], season_id=dct['season_id'])
        
    def to_dict(self):
        dct = super(BLBDivision, self).to_dict()
        dct['name'] = self.name
        dct['season_id'] = self.season_id
        dct['teams'] = [team.to_dict() for team in self.teams]
        return dct
    

class BLBTeam(Base):
    """BLB Teams"""
    __tablename__ = 'blb_team'

    id = Column(Integer, primary_key=True)
    location = Column(String(30))
    nickname = Column(String(30))
    abbreviation = Column(String(4))

    # Maps to authenticated account
    account = Column(String(32), nullable=True)

    # One BLBDivision to Many BLBTeams
    division_id = Column(Integer, ForeignKey('blb_division.id'))
    division = relationship('BLBDivision', back_populates='teams')

    # One BLBSeason to Many BLBTeams
    season_id = Column(Integer, ForeignKey('blb_season.id'))
    season = relationship('BLBSeason', back_populates='teams')
    
    def __repr__(self):
        return "<BLBTeam({} {})>".format(self.location, self.nickname)

    @classmethod
    def from_dict(cls, dct):
        return cls(
            location=dct['location'],
            nickname=dct['nickname'],
            abbreviation=dct['abbreviation'],
            division_id=dct['division_id'],
            season_id=dct['season_id']
        )
    
    def to_dict(self):
        dct = super(BLBTeam, self).to_dict()
        dct['location'] = self.location
        dct['nickname'] = self.nickname
        dct['abbreviation'] = self.abbreviation
        dct['division_id'] = self.division_id
        dct['season_id'] = self.season_id
        return dct


def BLBRoster(Base):
    """BLB Roster"""


class BLBPlayer(Base):
    """BLB Player"""
    __tablename__ = 'blb_player'

    id = Column(Integer, primary_key=True)

    # One FGPlayer to Many BLBPlayers
    fg_player_id = Column(Integer, ForeignKey('fg_player.id'))
    fg_player = relationship('FGPlayer')
