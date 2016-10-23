import tornado.ioloop
import tornado.web

from data.sql_store import SQLStore
from web.handlers import (
    BLBDivisionHandler,
    BLBLeagueHandler,
    BLBSeasonHandler,
    BLBTeamHandler,
    FGPlayersHandler,
    FGBattingHandler,
    FGPitchingHandler,
    FGSeasonsHandler
)

PORT=9191

class TornadoApp(tornado.web.Application):
    def __init__(self):
        routes = [
            # BLB API
            (r'/blb/divisions[/]?', BLBDivisionHandler),
            (r'/blb/divisions/(\d*)[/]?', BLBDivisionHandler),
            (r'/blb/leagues[/]?', BLBLeagueHandler),
            (r'/blb/seasons[/]?', BLBSeasonHandler),
            (r'/blb/seasons/(\d*)[/]?', BLBSeasonHandler),
            (r'/blb/teams[/]?', BLBTeamHandler),
            (r'/blb/teams/(\d*)/?', BLBTeamHandler),

            # Fangraphs API
            (r'/fg/players[/]?', FGPlayersHandler),
            (r'/fg/players/(\d*)[/]?', FGPlayersHandler),
            (r'/fg/batting/(\d*)[/]?', FGBattingHandler),
            (r'/fg/pitching/(\d*)[/]?', FGPitchingHandler),
            (r'/fg/seasons[/]?', FGSeasonsHandler)
        ]
        settings = { 'debug': True }
        tornado.web.Application.__init__(self, routes, **settings)

def main(args):
    application = TornadoApp()
    application.store = SQLStore()
    application.listen(PORT)
    print "Listening on %d" % (PORT)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="The Strat web service")
    args = parser.parse_args()
    main(args)
