import json
import tornado.web
from tornado import gen

from data.sql_store import SQLStore
from data.exceptions import (
    InvalidLeagueException,
    InvalidPlayerException,
    InvalidYearException
)

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, Cache-Control")


    def write_error(self, status_code, **kwargs):
        data = {
            'status_code': status_code
        }
        self.write(json.dumps(data))
        self.finish()

    @gen.coroutine
    def options(self):
        self.set_status(204)
        self.finish()


class BLBLeagueHandler(BaseHandler):

    SUPPORTED_METHODS = ('GET', 'POST', 'OPTIONS')

    @gen.coroutine
    def get(self, league_id=None):
        leagues = None
        try:
            if league_id is None:
                leagues = yield self.application.store.get_blb_leagues()
            else:
                league = yield self.application.store.get_blb_league(league_id)
                if league is not None:
                    leagues = [league]
        except InvalidLeagueException:
            pass
        
        self.write(json.dumps(leagues if leagues is not None else []))
        self.finish()

    @gen.coroutine
    def post(self):
        self.application.store.create_blb_league(json.loads(self.request.body))
        self.finish()


class BLBSeasonHandler(BaseHandler):
    
    SUPPORTED_METHODS = ('GET', 'POST', 'OPTIONS')

    @gen.coroutine
    def get(self, season_id=None):
        league_id = self.get_argument('league_id', None)
        seasons = []
        if season_id is not None:
            result = yield self.application.store.get_blb_season_by_season_id(season_id)
            if result is not None:
                seasons = [result]
        elif league_id is not None:
            seasons = yield self.application.store.get_blb_seasons_by_league_id(league_id)
        self.write(json.dumps(seasons if seasons is not None else []))
        self.finish()

    @gen.coroutine
    def post(self):
        self.application.store.create_blb_season(json.loads(self.request.body))
        self.finish()


class BLBTeamHandler(BaseHandler):

    SUPPORTED_METHODS = ('GET', 'POST')

    @gen.coroutine
    def get(self, team_id=None):
        division_id = self.get_argument('division_id', None)
        season_id = self.get_argument('season_id', None)
        teams = []
        if team_id is not None:
            result = yield self.application.store.get_blb_team_by_team_id(team_id)
            if result is not None:
                teams = [result]
        elif division_id is not None:
            teams = yield self.application.store.get_blb_teams_by_division_id(division_id)
        elif season_id is not None:
            teams = yield self.application.store.get_blb_teams_by_season_id(season_id)
        self.write(json.dumps(teams if teams is not None else []))
        self.finish()

    @gen.coroutine
    def post(self):
        self.application.store.create_blb_team(json.loads(self.request.body))
        self.finish()


class BLBDivisionHandler(BaseHandler):

    SUPPORTED_METHODS = ('GET', 'POST')

    @gen.coroutine
    def get(self, division_id=None):
        season_id = self.get_argument('season_id', None)
        divisions = []
        if division_id is not None:
            result = yield self.application.store.get_blb_division_by_division_id(division_id)
            if result is not None:
                divisions = [result]
        elif season_id is not None:
            divisions = yield self.application.store.get_blb_division_by_season_id(season_id)
        self.write(json.dumps(divisions if divisions is not None else []))
        self.finish()

    @gen.coroutine
    def post(self):
        self.application.store.create_blb_division(json.loads(self.request.body))
        self.finish()

class FGSeasonsHandler(BaseHandler):

    SUPPORTED_METHODS = ('GET')

    @gen.coroutine
    def get(self):
        seasons = yield self.application.store.get_fg_seasons()
        self.write(json.dumps(seasons if seasons is not None else []))
        self.finish()

class FGPlayersHandler(BaseHandler):

    SUPPORTED_METHODS = ('GET')
    
    @gen.coroutine
    def get(self, player_id=None):
        year = self.get_argument('year', None)

        players = None
        try:
            if player_id is None:
                players = yield self.application.store.get_fg_players_by_year(year)
            else:
                player = yield self.application.store.get_fg_player(player_id, year)
                if player is not None:
                    players = [player]
        except InvalidPlayerException:
            pass
        except InvalidYearException:
            pass
            
        if players is None:
            self.send_error(404)
            raise gen.Return()
        
        self.write(json.dumps(players if players is not None else []))
        self.finish()

        
class FGBattingHandler(BaseHandler):

    SUPPORTED_METHODS = ('GET')

    @gen.coroutine
    def get(self, player_id=None):
        year = self.get_argument('year', None)

        try:
            if player_id is None:
                batting = yield self.application.store.get_fg_batting_by_year(year)
            else:
                batting = yield self.application.store.get_fg_batting_by_player(player_id)
                if year is not None:
                    batting = [b for b in batting if b['season'] == year]
        except InvalidPlayerException:
            pass
        except InvalidYearException:
            pass
        
        if batting is None or len(batting) == 0:
            self.send_error(404)
            raise gen.Return()
        
        self.write(json.dumps(batting))
        self.finish


class FGPitchingHandler(BaseHandler):

    SUPPORTED_METHODS = ('GET')

    @gen.coroutine
    def get(self, year):
        pitching = yield self.application.store.get_fg_pitching_by_year(year)
        if pitching is None:
            self.send_error(404, msg='Not Found')
            raise gen.Return()
        
        self.write(json.dumps(pitching))
        self.finish()
