from sqlalchemy import ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.types import Boolean, Date, Enum

from .core import Base
from .fangraphs import FGPlayer, FGSeason


class BLBLeague(Base):
    """BLB Leagues"""
    __tablename__ = 'blb_league'
    __table_args__ = (
        UniqueConstraint('name'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    abbreviation = Column(String(10))

    # Many BLBSeasons to One BLBLeague
    seasons = relationship('BLBSeason', back_populates='league')

    def __repr__(self):
        return "<BLBLeague({} {})>".format(self.name, self.abbreviation)

    @classmethod
    def from_dict(cls, dct):
        return cls(name=dct['name'], abbreviation=dct['abbreviation'])
    
    def to_dict(self):
        dct = super(BLBLeague, self).to_dict()
        dct['name'] = self.name
        dct['abbreviation'] = self.abbreviation
        dct['seasons'] = [season.to_dict() for season in self.seasons]
        return dct


class BLBSeason(Base):
    """BLB Seasons"""
    __tablename__ = 'blb_season'
    __table_args__ = (
        UniqueConstraint('fg_season_id', 'league_id', 'name'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)

    fg_season_id = Column(Integer, ForeignKey('fg_season.id'))
    fg_season = relationship('FGSeason')

    # One BLBLeague to Many BLBSeasons
    league_id = Column(Integer, ForeignKey('blb_league.id'))
    league = relationship('BLBLeague', back_populates='seasons')

    # Many BLBDivisions to One BLBSeason
    divisions = relationship('BLBDivision', back_populates='season')

    # Many BLBTeams to One BLBSeason
    teams = relationship('BLBTeam', back_populates='season')

    # Many BLBGames to One BLBSeason
    games = relationship('BLBGame', back_populates='season')

    def __repr__(self):
        if self.name is not None:
            return "<BLBSeason({} {})>".format(self.year, self.name)
        else:
            return "<BLBSeason({})>".format(self.year)

    @classmethod
    def from_dict(cls, dct):
        return cls(
            fg_season_id=dct['fg_season_id'],
            name=dct['name'],
            league_id=dct['league_id'])
    
    def to_dict(self):
        dct = super(BLBSeason, self).to_dict()
        dct['fg_season_id'] = self.fg_season_id
        dct['name'] = self.name
        dct['league_id'] = self.league_id
        dct['divisions'] = [division.to_dict() for division in self.divisions]
        dct['teams'] = [team.to_dict() for team in self.teams]
        return dct
        

class BLBDivision(Base):
    """BLB Divisions"""
    __tablename__ = 'blb_division'
    __table_args__ = (
        UniqueConstraint('season_id', 'name'),
    )

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
    __table_args__ = (
        UniqueConstraint('season_id', 'location', 'nickname'),
        UniqueConstraint('season_id', 'abbreviation')
    )

    id = Column(Integer, primary_key=True)
    location = Column(String(30))
    nickname = Column(String(30))
    abbreviation = Column(String(4))

    # One BLBDivision to Many BLBTeams
    division_id = Column(Integer, ForeignKey('blb_division.id'))
    division = relationship('BLBDivision', back_populates='teams')

    # One BLBSeason to Many BLBTeams
    season_id = Column(Integer, ForeignKey('blb_season.id'))
    season = relationship('BLBSeason', back_populates='teams')

    # Many BLBRosterEntries to One BLBTeam
    players = relationship('BLBRosterEntry', back_populates='team')

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


class BLBPlayer(Base):
    """BLB Player"""
    __tablename__ = 'blb_player'

    id = Column(Integer, primary_key=True)

    # One FGPlayer to Many BLBPlayers
    fg_player_id = Column(Integer, ForeignKey('fg_player.id'))
    fg_player = relationship('FGPlayer')

    # Many BLBRosterEntries to one BLBPlayer
    blb_roster_entries = relationship('BLBRosterEntry')


class BLBRosterEntry(Base):
    """BLB Roster"""
    __tablename__ = 'blb_roster_entry'

    id = Column(Integer, primary_key=True)

    # One BLBPlayer to Many BLBRosterEntries
    player_id = Column(Integer, ForeignKey('blb_player.id'))
    player = relationship('BLBPlayer', back_populates='blb_roster_entries')

    # One BLBTeam to Many BLBRosterEntries
    team_id = Column(Integer, ForeignKey('blb_team.id'))
    team = relationship('BLBTeam', back_populates='players')

    blb_game_batting = relationship('BLBGameBatting', back_populates='roster_entry')

    blb_game_pitching = relationship('BLBGamePitching', back_populates='roster_entry')

    start_date = Column(Date)
    end_date = Column(Date, nullable=True)

    is_active = Column(Boolean)
    

class BLBGame(Base):
    """BLB Game"""
    __tablename__ = 'blb_game'

    # Metadata
    id = Column(Integer, primary_key=True)
    date = Column(Date) # mm/dd/yyyy
    attendance = Column(Integer)
    duration = Column(Integer) # minutes
    weather = Column(Enum('Good', 'Bad', 'Average'))
    time_of_day = Column(Enum('Day', 'Night'))

    # One BLBSeason to Many BLBGames
    season_id = Column(Integer, ForeignKey('blb_season.id'))
    season = relationship('BLBSeason', back_populates='games')
    
    # One BLBTeam to Many BLBGames
    home_team_id = Column(Integer, ForeignKey('blb_team.id'))
    home_team = relationship('BLBTeam', foreign_keys=[home_team_id])

    # One BLBTeam to Many BLBGames
    away_team_id = Column(Integer, ForeignKey('blb_team.id'))
    away_team = relationship('BLBTeam', foreign_keys=[away_team_id])

    blb_inning = relationship('BLBInning', back_populates='game')

    blb_game_batting = relationship('BLBGameBatting', back_populates='game')
    blb_game_pitching = relationship('BLBGamePitching', back_populates='game')

    # Game Details
    home_team_runs = Column(Integer)
    home_team_hits = Column(Integer)
    home_team_errors = Column(Integer)
    home_team_lob = Column(Integer)
    home_team_double_plays = Column(Integer)
    
    away_team_runs = Column(Integer)
    away_team_hits = Column(Integer)
    away_team_errors = Column(Integer)
    away_team_lob = Column(Integer)
    away_team_double_plays = Column(Integer)

    def __repr__(self):
        return "<BLBGame({} {})>".format(self.home, self.away)

    @classmethod
    def from_dict(cls, dct):
        return cls(
            date=dct['date'],
            attendance=dct['attendance'],
            duration=dct['duration'],
            weather=dct['weather'],
            time_of_day=dct['time_of_day'],
            home_team_id=dct['home_team_id'],
            away_team_id=dct['away_team_id']
        )


class BLBInning(Base):
    """BLB Inning details for a BLB Game"""
    __tablename__ = 'blb_inning'
    __table_args__ = (
        UniqueConstraint('number', 'half', 'game_id'),
        )

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    half = Column(Enum('Top', 'Bottom'))

    r = Column(Integer)

    game_id = Column(Integer, ForeignKey('blb_game.id'))
    game = relationship('BLBGame', back_populates='blb_inning')
    
    def __repr__(self):
        return "<BLBInning({} {})>".format(self.half, self.number)

    @classmethod
    def from_dict(self, dct):
        return cls(
            number=dct['number'],
            half=dct['half'],
            r=dct['runs'],
            game_id=dct['game_id']
            )

    
class BLBGameBatting(Base):
    """BLB Batting stats for a BLB Game"""
    __tablename__ = 'blb_game_batting'
    __table_args__ = (
        UniqueConstraint('roster_entry_id', 'game_id'),
    )

    id = Column(Integer, primary_key=True)

    roster_entry_id = Column(Integer, ForeignKey('blb_roster_entry.id'))
    roster_entry = relationship('BLBRosterEntry', back_populates='blb_game_batting')

    game_id = Column(Integer, ForeignKey('blb_game.id'))
    game = relationship('BLBGame', back_populates='blb_game_batting')

    ab = Column(Integer)
    pa = Column(Integer)
    r = Column(Integer)
    h = Column(Integer)
    bb = Column(Integer)
    ibb = Column(Integer)
    so = Column(Integer)
    rbi = Column(Integer)
    single = Column(Integer)
    double = Column(Integer)
    triple = Column(Integer)
    hr = Column(Integer)
    sb = Column(Integer)
    cs = Column(Integer)
    hbp = Column(Integer)
    gdp = Column(Integer)


class BLBGamePitching(Base):
    """BLB Pitching stats for a BLB Game"""
    __tablename__ = 'blb_game_pitching'
    __table_args__ = (
        UniqueConstraint('roster_entry_id', 'game_id'),
    )

    id = Column(Integer, primary_key=True)

    roster_entry_id = Column(Integer, ForeignKey('blb_roster_entry.id'))
    roster_entry = relationship('BLBRosterEntry', back_populates='blb_game_pitching')

    game_id = Column(Integer, ForeignKey('blb_game.id'))
    game = relationship('BLBGame', back_populates='blb_game_pitching')
    
    ip = Column(Integer) # Outs recorded, e.g. 1 2/3 IP = 5 Outs
    h = Column(Integer)
    r = Column(Integer)
    er = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    hr = Column(Integer)
    pc = Column(Integer)
    
