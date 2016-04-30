from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, Integer, String

from .core import Base

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
