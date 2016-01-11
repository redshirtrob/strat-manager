import json
import tornado.web
from tornado import gen

from data.sql_store import SQLStore
from data.exceptions import (InvalidPlayerException, InvalidYearException)

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-type', 'application/json')

    def write_error(self, status_code, **kwargs):
        data = {
            'status_code': status_code
        }
        self.write(json.dumps(data))
        self.finish()

class PlayersHandler(BaseHandler):

    SUPPORTED_METHODS = ('GET')
    
    @gen.coroutine
    def get(self, player_id=None):
        year = self.get_argument('year', None)

        players = None
        try:
            if player_id is None:
                players = yield self.application.store.get_players_by_year(year)
            else:
                player = yield self.application.store.get_player(player_id, year)
                if player is not None:
                    players = [player]
        except InvalidPlayerException:
            pass
        except InvalidYearException:
            pass
            
        if players is None:
            self.send_error(404)
            raise gen.Return()
        
        self.write(json.dumps(players))
        self.finish()

        
class BattingHandler(BaseHandler):

    SUPPORTED_METHODS = ('GET')

    @gen.coroutine
    def get(self, player_id=None):
        year = self.get_argument('year', None)

        try:
            if player_id is None:
                batting = yield self.application.store.get_batting_by_year(year)
            else:
                batting = yield self.application.store.get_batting_by_player(player_id)
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


class PitchingHandler(BaseHandler):

    SUPPORTED_METHODS = ('GET')

    @gen.coroutine
    def get(self, year):
        pitching = yield self.application.store.get_pitching_by_year(year)
        if pitching is None:
            self.send_error(404, msg='Not Found')
            raise gen.Return()
        
        self.write(json.dumps(pitching))
        self.finish()
