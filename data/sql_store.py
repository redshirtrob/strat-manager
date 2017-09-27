from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from tornado import gen

from blb.models.fangraphs import (
    FGSeason,
    FGPlayer, 
    FGPlayerSeason,
    FGBatting,
    FGPitching,
    FGTeam
)

from blb.models.blb import (
    BLBDivision,
    BLBLeague,
    BLBSeason,
    BLBTeam
)

from .exceptions import (
    InvalidLeagueException,
    InvalidPlayerException,
    InvalidYearException
)


class SQLStore(object):

    def __init__(self, db_file='blb.db'):
        self.ENGINE = create_engine('sqlite:///{}'.format(db_file))
        self.Session = sessionmaker(bind=self.ENGINE)
        self.session = self.Session()

    @gen.coroutine
    def create_blb_league(self, dct):
        """Create a BLB League"""
        
        blb_league = BLBLeague.from_dict(dct)
        self.session.add(blb_league)
        self.session.commit()
        raise gen.Return()

    @gen.coroutine
    def get_or_create_blb_league(self, dct):
        league = self.session.query(BLBLeague).filter(BLBLeague.name == dct['name']).one_or_none()
        if league is None:
            league = BLBLeague.from_dict(dct)
            self.session.add(league)
            self.session.commit()
        raise gen.Return(league)

    @gen.coroutine
    def get_blb_leagues(self):
        """Get all BLB Leagues"""
        
        results = self.session.query(BLBLeague).all()
        if results:
            leagues = [league.to_dict() for league in results]
            raise gen.Return(leagues)

    @gen.coroutine
    def get_blb_league_by_id(self, league_id=None):
        """Get a BLB League"""

        if league_id is None:
            raise InvalidLeagueException("You must specify a league id")

        league = self.session.query(BLBLeague).one_or_none(BLBLeague.id == league_id)
        raise gen.Return(league.to_dict)

    @gen.coroutine
    def create_blb_season(self, dct):
        """Create a BLB Season"""
        
        blb_season = BLBSeason.from_dict(dct)
        self.session.add(blb_season)
        self.session.commit()
        raise gen.Return()

    @gen.coroutine
    def get_or_create_blb_season(self, dct):
        fg_season = self.session.query(FGSeason).filter(FGSeason.year == dct['year']).one_or_none()
        
        season = self.session.query(BLBSeason).filter(and_(
            BLBSeason.league_id == dct['league_id'],
            BLBSeason.name == dct['name'])
        ).one_or_none()
        if season is None:
            dct['fg_season_id'] = fg_season.id
            season = BLBSeason.from_dict(dct)
            self.session.add(season)
            self.session.commit()
        raise gen.Return(season)

    @gen.coroutine
    def get_blb_seasons_by_league_id(self, league_id):
        """Get all seasons in a league"""
        
        results = self.session.query(BLBSeason).filter(BLBSeason.league_id == league_id).all()
        if results is not None:
            seasons = [season.to_dict() for season in results]
            raise gen.Return(seasons)

    @gen.coroutine
    def get_blb_season_by_season_id(self, season_id):
        """Get a season"""

        season = self.session.query(BLBSeason).get(season_id)
        if season is not None:
            raise gen.Return(season.to_dict())

    @gen.coroutine
    def create_blb_division(self, dct):
        "Create a BLB Division"

        blb_division = BLBDivision.from_dict(dct)
        self.session.add(blb_division)
        self.session.commit()
        raise gen.Return()

    @gen.coroutine
    def get_or_create_blb_division(self, dct):
        division = self.session.query(BLBDivision).filter(and_(
            BLBDivision.name == dct['name'],
            BLBDivision.season_id == dct['season_id'])
        ).one_or_none()
        if division is None:
            division = BLBDivision.from_dict(dct)
            self.session.add(division)
            self.session.commit()
        raise gen.Return(division)

    @gen.coroutine
    def get_blb_division_by_division_id(self, division_id=None):
        """Get a BLB Division based on the division id"""

        division = self.session.query(BLBDivision).get(division_id)
        if division is not None:
            raise gen.Return(division.to_dict())

    @gen.coroutine
    def get_blb_division_by_season_id(self, season_id=None):
        """Get all divisions in a season"""

        results = self.session.query(BLBDivision).filter(BLBDivision.season_id == season_id).all()
        if results is not None:
            divisions = [division.to_dict() for division in results]
            raise gen.Return(divisions)

    @gen.coroutine
    def create_blb_team(self, dct):
        "Create a BLB Team"

        blb_team = BLBTeam.from_dict(dct)
        self.session.add(blb_team)
        self.session.commit()
        raise gen.Return()

    @gen.coroutine
    def get_or_create_blb_team(self, dct):
        team = self.session.query(BLBTeam).filter(and_(
            BLBTeam.location == dct['location'],
            BLBTeam.nickname == dct['nickname'],
            BLBTeam.abbreviation == dct['abbreviation'],
            BLBTeam.season_id == dct['season_id']
            )).one_or_none()
        if team is None:
            team = BLBTeam.from_dict(dct)
            self.session.add(team)
            self.session.commit()
        raise gen.Return(team)


    @gen.coroutine
    def get_blb_team_by_team_id(self, team_id=None):
        "Get a BLB Team based on the team id"

        team = self.session.query(BLBTeam).get(team_id)
        if team is not None:
            raise gen.Return(team.to_dict())

    @gen.coroutine
    def get_blb_teams_by_division_id(self, division_id=None):
        "Get all BLB Teams in a division"

        results = self.session.query(BLBTeam).filter(BLBTeam.division_id == division_id).all()
        if results is not None:
            teams = [team.to_dict() for team in results]
            raise gen.Return(teams)

    @gen.coroutine
    def get_blb_teams_by_season_id(self, season_id=None):
        "Get all BLB Teams in a season"

        results = self.session.query(BLBTeam).filter(BLBTeam.season_id == season_id).all()
        if results is not None:
            teams = [team.to_dict() for team in results]
            raise gen.Return(teams)

    @gen.coroutine
    def get_fg_seasons(self):
        """Get a list of all seasons"""
        
        results = self.session.query(FGSeason).all()
        if results:
            seasons = [s.to_dict() for s in results]
            raise gen.Return(seasons)

    @gen.coroutine
    def get_fg_season_by_year(self, year=None):
        """Get a single season"""
        
        results = self.session.query(FGSeason).all()
        if results:
            seasons = [s.to_dict() for s in results]
            raise gen.Return(seasons)
        
    @gen.coroutine
    def get_fg_players_by_year(self, year=None):
        """Get a list of all players"""
        
        if year is None:
            raise InvalidYearException("You must specify a year")

        player_seasons = self.session.query(FGPlayerSeason).join(FGSeason).filter(and_(
            FGSeason.id == FGPlayerSeason.season_id,
            FGSeason.year == year)
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
    def get_fg_player(self, player_id=None, year=None):
        if player_id is None:
            raise InvalidPlayerException("You must specify a player")

        player_seasons = self.session.query(FGPlayerSeason).filter(FGPlayerSeason.player_id == player_id)
        if year is not None:
            player_seasons = player_seasons.join(FGSeason).filter(and_(
                FGPlayerSeason.season_id == FGSeason.id,
                FGSeason.year == year)
            )
        player_seasons = player_seasons.all()

        if len(player_seasons) > 0:
            player = player_seasons[0].player.to_dict()
            player['batting'] = [ps.batting.to_dict() for ps in player_seasons if ps.batting is not None]
            player['pitching'] = [ps.pitching.to_dict() for ps in player_seasons if ps.pitching is not None]
            raise gen.Return(player)

    @gen.coroutine
    def get_fg_batting_by_year(self, year=None):
        """Get a list of all batting statistics"""
        
        if year is None:
            raise InvalidYearException("You must specify a year")
        
        results = self.session.query(FGBatting).join(FGPlayerSeason).join(FGSeason).filter(and_(
            FGBatting.player_season_id == FGPlayerSeason.id,
            FGPlayerSeason.season_id == FGSeason.id,
            FGSeason.year == year)
        ).all()

        if results:
            batting = [b.to_dict() for b in results]
            raise gen.Return(batting)

    @gen.coroutine
    def get_fg_batting_by_player(self, player_id=None):
        """Get all batting statistics for a given player"""

        if player_id is None:
            raise InvalidPlayerException("You must specify a player")
            
        results = self.session.query(FGBatting).join(FGPlayerSeason).join(FGPlayer).filter(and_(
            FGBatting.player_season_id == FGPlayerSeason.id, FGPlayer.id == player_id
        )).all()

        if results:
            batting = [b.to_dict() for b in results]
            raise gen.Return(batting)

    @gen.coroutine
    def get_fg_pitching_by_year(self, year=None):
        """Get a list of all pitching statistics"""
        
        if year is None:
            raise InvalidYearException("You must specify a year")
        
        results = self.session.query(FGPitching).join(FGPlayerSeason).join(FGSeason).filter(and_(
            FGPitching.player_season_id == FGPlayerSeason.id, FGSeason.year == year)
        ).all()

        if results:
            pitching = [p.to_dict() for p in results]
            raise gen.Return(pitching)

    @gen.coroutine
    def get_fg_pitching_by_player(self, player_id=None):
        """Get all pitching statistics for a given player"""

        if player_id is None:
            raise InvalidPlayerException("You must specify a player")
            
        results = self.session.query(FGPitching).join(FGPlayerSeason).join(FGPlayer).filter(and_(
            FGPitching.player_season_id == FGPlayerSeason.id, FGPlayer.id == player_id
        )).all()

        if results:
            pitching = [p.to_dict() for p in results]
            raise gen.Return(pitching)
    

