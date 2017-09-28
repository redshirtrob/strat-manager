#!/usr/bin/env python

import json

from datetime import datetime

from data.sql_store import SQLStore
from blb.models.blb import BLBGame

DOUBLE_PLAYS="DOUBLE PLAYS"
TRIPLE_PLAYS="TRIPLE PLAYS"
LEFT_ON_BASE="LEFT ON BASE"

class Boxscore(object):

    def __init__(self, boxscore, store, league_name):
        self.boxscore = boxscore
        self.store = store
        self.league = self.store.get_blb_league_by_name(league_name).result()

    def get_value_for_team(self, team, value_type):
        tsd = self.boxscore['team_statistics_details']
        return next((int(x[team]['count']) for x in tsd if x['name'] == value_type), 0)

    def get_box_value_for_team(self, nickname, value_type):
        team_boxscore = self.boxscore['team_boxscore']
        return next((int(x['totals'][value_type]) for x in team_boxscore if x['nickname'] == nickname), 0)

    def get_game_dict(self):
        matchup = self.boxscore['matchup']
        date = datetime.strptime(matchup['date'], '%m/%d/%Y').date()
        home_team = self.store.get_blb_team(matchup['home'], self.league.id).result()
        away_team = self.store.get_blb_team(matchup['away'], self.league.id).result()

        assert(home_team.season_id == away_team.season_id)

        pd = self.boxscore['peripheral_game_data']
        attendance = int(pd['attendance'].replace(',', ''))
        duration = int(pd['duration']['hours']) * 60 + int(pd['duration']['minutes'])
        weather = pd['weather']
        time_of_day = pd['time']

        tsd = self.boxscore['team_statistics_details']

        return {
            'date': date,
            'attendance': attendance,
            'duration': duration,
            'weather': weather,
            'time_of_day': time_of_day,

            'season_id': home_team.season_id,

            'home_team_id': home_team.id,
            'home_team_lob': self.get_value_for_team('home', LEFT_ON_BASE),
            'home_team_double_plays': self.get_value_for_team('home', DOUBLE_PLAYS),
            'home_team_triple_plays': self.get_value_for_team('home', TRIPLE_PLAYS),
            'home_team_runs': self.get_box_value_for_team(home_team.nickname, 'runs'),
            'home_team_hits': self.get_box_value_for_team(home_team.nickname, 'hits'),
            'home_team_errors': self.get_box_value_for_team(home_team.nickname, 'errors'),
            
            'away_team_id': away_team.id,
            'away_team_lob': self.get_value_for_team('away', LEFT_ON_BASE),
            'away_team_double_plays': self.get_value_for_team('away', DOUBLE_PLAYS),
            'away_team_triple_plays': self.get_value_for_team('away', TRIPLE_PLAYS),
            'away_team_runs': self.get_box_value_for_team(away_team.nickname, 'runs'),
            'away_team_hits': self.get_box_value_for_team(away_team.nickname, 'hits'),
            'away_team_errors': self.get_box_value_for_team(away_team.nickname, 'errors')
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
        try:
            blb_game = BLBGame.from_dict(game_dict)
            store.session.add(blb_game)
            store.session.commit()
        except Exception:
            store.session.rollback()
        

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Populate BLB games from input file")
    parser.add_argument('db', metavar='DB', help='the DB file')
    parser.add_argument('file', metavar="FILE", help="the input file")
    args = parser.parse_args()
    
    main(args.db, args.file, 'Big League Baseball')
