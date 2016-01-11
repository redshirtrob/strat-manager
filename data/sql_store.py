from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from tornado import gen

from blb.models.fangraphs import (Season, Player, 
    PlayerSeason, Batting, Pitching, Team)

from .exceptions import (InvalidPlayerException, InvalidYearException)

ENGINE = create_engine('sqlite:///blb.db')
Session = sessionmaker(bind=ENGINE)
session = Session()

class SQLStore(object):

    def __init__(self):
        self.session = Session()

    @gen.coroutine
    def get_seasons(self):
        """Get a list of all seasons"""
        
        results = self.session.query(Season).all()
        if results:
            seasons = [s.to_dict() for s in results]
            raise gen.Return(seasons)

    @gen.coroutine
    def get_players_by_year(self, year=None):
        """Get a list of all players"""
        
        if year is None:
            raise InvalidYearException("You must specify a year")

        player_seasons = self.session.query(PlayerSeason).join(Season).filter(
            Season.id == PlayerSeason.season_id
        ).filter(
            Season.year == year
        ).all()

        if player_seasons:
            results = [ps.player for ps in player_seasons]
            players = [r.to_dict() for r in results]
            raise gen.Return(players)

    @gen.coroutine
    def get_batting_by_year(self, year=None):
        """Get a list of all batting statistics"""
        
        if year is None:
            raise InvalidYearException("You must specify a year")
        
        results = session.query(Batting).join(PlayerSeason).join(Season).filter(and_(
            Batting.player_season_id == PlayerSeason.id, Season.year == year)
        ).all()

        if results:
            batting = [b.to_dict() for b in results]
            raise gen.Return(batting)

    @gen.coroutine
    def get_batting_by_player(self, player_id=None):
        """Get all batting statistics for a given player"""

        if player_id is None:
            raise InvalidPlayerException("You must specify a player")
            
        results = self.session.query(Batting).join(PlayerSeason).join(Player).filter(and_(
            Batting.player_season_id == PlayerSeason.id, Player.id == player_id
        )).all()

        if results:
            batting = [b.to_dict() for b in results]
            raise gen.Return(batting)

    @gen.coroutine
    def get_pitching_by_year(self, year=None):
        """Get a list of all pitching statistics"""
        
        if year is None:
            raise InvalidYearException("You must specify a year")
        
        results = session.query(Pitching).join(PlayerSeason).join(Season).filter(and_(
            Pitching.player_season_id == PlayerSeason.id, Season.year == year)
        ).all()

        if results:
            pitching = [p.to_dict() for p in results]
            raise gen.Return(pitching)

    @gen.coroutine
    def get_pitching_by_player(self, player_id=None):
        """Get all pitching statistics for a given player"""

        if player_id is None:
            raise InvalidPlayerException("You must specify a player")
            
        results = self.session.query(Pitching).join(PlayerSeason).join(Player).filter(and_(
            Pitching.player_season_id == PlayerSeason.id, Player.id == player_id
        )).all()

        if results:
            pitching = [p.to_dict() for p in results]
            raise gen.Return(pitching)
    

