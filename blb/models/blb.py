from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, Integer, String

from blb.models.core import Base

class BLBLeague(Base):
    """BLB Leagues"""
    __tablename__ = 'blb_league'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    abbreviation = Column(String(10))


class BLBSeason(Base):
    """BLB Seasons"""
    __tablename__ = 'blb_season'

    id = Column(Integer, primary_key=True)
    year = Column(String(4))
    name = Column(String(50))

    # One BLBLeague to many Seasons
    league = relationship('BLBLeague', back_populates='seasons')


class BLBDivision(Base):
    """BLB Divisions"""
    __tablename__ = 'blb_division'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    # One BLBSeason to many Divisions
    season = relationship('BLBSeason', back_populates='divisions')


class BLBTeam(Base):
    """BLB Teams"""
    __tablename__ = 'blb_team'

    id = Column(Integer, primary_key=True)
    location = Column(String(30))
    nickname = Column(String(30))
    abbreviation = Column(String(4))

    # Maps to authenticated account
    account = Column(String(32), nullable=True)

    # One BLBDivision to many Teams
    division = relationship('BLBDivision', back_populates='teams')

    # One BLBSeason to many Teams
    season = relationship('BLBSeason', back_populates='teams')
    
