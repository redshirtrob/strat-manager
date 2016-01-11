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

        player_seasons = self.session.query(PlayerSeason).join(Season).filter(and_(
            Season.id == PlayerSeason.season_id,
            Season.year == year)
        ).all()

        if player_seasons:
            players = []
            for ps in player_seasons:
                player = ps.player.to_dict()
                if ps.batting is not None:
                    player['batting'] = [ps.batting.to_dict()]
                if ps.pitching is not None:
                    player['pitching'] = [ps.pitching.to_dict()]
                players.append(player)
            raise gen.Return(players)

    @gen.coroutine
    def get_player(self, player_id=None, year=None):
        if player_id is None:
            raise InvalidPlayerException("You must specify a player")

        player_seasons = self.session.query(PlayerSeason).filter(PlayerSeason.player_id == player_id)
        if year is not None:
            player_seasons = player_seasons.join(Season).filter(and_(
                PlayerSeason.season_id == Season.id,
                Season.year == year)
            )
        player_seasons = player_seasons.all()

        if len(player_seasons) > 0:
            player = player_seasons[0].player.to_dict()
            player['batting'] = [ps.batting.to_dict() for ps in player_seasons if ps.batting is not None]
            player['pitching'] = [ps.pitching.to_dict() for ps in player_seasons if ps.pitching is not None]
            raise gen.Return(player)

    @gen.coroutine
    def get_batting_by_year(self, year=None):
        """Get a list of all batting statistics"""
        
        if year is None:
            raise InvalidYearException("You must specify a year")
        
        results = session.query(Batting).join(PlayerSeason).join(Season).filter(and_(
            Batting.player_season_id == PlayerSeason.id,
            PlayerSeason.season_id == Season.id,
            Season.year == year)
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
    

