#!/usr/bin/env python

import json

from datetime import datetime

from data.sql_store import SQLStore


class Boxscore(object):

    def __init__(self, boxscore, store, league_name):
        self.boxscore = boxscore
        self.store = store
        self.league = self.store.get_blb_league_by_name(league_name).result()

    def get_game_dict(self):
        matchup = self.boxscore['matchup']
        date = datetime.strptime(matchup['date'], '%m/%d/%Y').date()
        home_team = self.store.get_blb_team(matchup['home'], self.league.id).result()
        away_team = self.store.get_blb_team(matchup['away'], self.league.id).result()

        pd = self.boxscore['peripheral_game_data']
        attendance = int(pd['attendance'].replace(',', ''))
        duration = int(pd['duration']['hours']) * 60 + int(pd['duration']['minutes'])
        weather = pd['weather']
        time_of_day = pd['time']

        return {
            'date': date,
            'attendance': attendance,
            'duration': duration,
            'weather': weather,
            'time_of_day': time_of_day,
            'home_team_id': home_team.id,
            'away_team_id': away_team.id
        }


def main(db_file, data_file, league_name):
    store = SQLStore(db_file)
    
    with open(data_file) as fp:
        league_dict = json.load(fp)

    # Create Games
    boxscores = league_dict['boxscores']
    for bs in boxscores:
        boxscore = Boxscore(bs, store, league_name)
        game_dict = boxscore.get_game_dict()
        print game_dict
        

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Populate BLB games from input file")
    parser.add_argument('db', metavar='DB', help='the DB file')
    parser.add_argument('file', metavar="FILE", help="the input file")
    args = parser.parse_args()
    
    main(args.db, args.file, 'Big League Baseball')
