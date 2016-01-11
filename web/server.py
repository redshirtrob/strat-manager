import tornado.ioloop
import tornado.web

from data.sql_store import SQLStore
from web.handlers import (PlayersHandler, BattingHandler, PitchingHandler)

PORT=9191

class TornadoApp(tornado.web.Application):
    def __init__(self):
        routes = [
            (r'/mlb/players/[/]?', PlayersHandler),
            (r'/mlb/players/(\d*)[/]?', PlayersHandler),
            (r'/mlb/batting/(\d*)[/]?', BattingHandler),
            (r'/mlb/pitching/(\d*)[/]?', PitchingHandler)
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
