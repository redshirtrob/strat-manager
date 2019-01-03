#!/usr/bin/env python

from datetime import datetime
import json
import os

from strat.parse import parse_league_daily, parse_game_daily
from strat.utils import get_report_type, get_title, flatten
from strat.utils import REPORT_TYPE_LEAGUE_DAILY, REPORT_TYPE_GAME_DAILY

CITIES = [
    'Atlanta',
    'Boston',
    'Charlotte',
    'Chicago',
    'Cincinnati',
    'Cleveland',
    'Columbus',
    'Detroit',
    'Miami',
    'Montreal',
    'Nashville',
    'New Orleans',
    'New York',
    'Philadelphia',
    'St. Louis',
    'Saint Louis',
    'Steel City',
    'Washington'
]

NICKNAMES = [
    'Crackers',
    'Blues',
    'Monarchs',
    'Northsiders',
    'Steamers',
    'Spiders',
    'Explorers',
    'Clutch',
    'Toros',
    'Souterrains',
    'Cats',
    'Mudbugs',
    'Knights',
    'Admirals',
    'Clydesdales',
    'Stogies',
    'Federals'
]

HOF_CITIES = [
    'Mt. Washington',
    'Mudville',
    'Sirk City',
    'Hackensack',
    'Motor City',
    'Cook County',
    'Vegas',
    'New Milan'
]

HOF_NICKNAMES = [
    'Wonders',
    'Grey Eagles',
    'Spikes',
    'Monuments',
    'Bulls',
    'Robber Barons',
    'Sultans',
    'Rajahs'
]


def report_type_string(report_type):
    if report_type == REPORT_TYPE_GAME_DAILY:
        return 'game-daily'
    elif report_type == REPORT_TYPE_LEAGUE_DAILY:
        return 'league-daily'
    else:
        return 'unknown'

def main(filename, stash_directory=None, league='blb'):
    should_stash = stash_directory is not None

    if league == 'blb':
        cities = CITIES
        nicknames = NICKNAMES
    elif league == 'hof':
        cities = HOF_CITIES
        nicknames = HOF_NICKNAMES
    
    with open(filename, 'r') as f:
        html = f.read()

    report_type = get_report_type(html)
    if report_type == REPORT_TYPE_LEAGUE_DAILY:
        ast = parse_league_daily(html, cities=cities, nicknames=nicknames)
    elif report_type == REPORT_TYPE_GAME_DAILY:
        ast = parse_game_daily(html, cities=cities, nicknames=nicknames)
    else:
        return

    flat_ast = flatten(ast)

    if should_stash:
        rootname = os.path.splitext(os.path.basename(filename))[0]
        matchup_datetime = datetime.strptime(flat_ast['boxscores'][0]['matchup']['date'], '%m/%d/%Y')
        dst_filename = '{}-{}-{}-ast.dat'.format(
            matchup_datetime.strftime('%Y-%m-%d'),
            report_type_string(report_type),
            rootname
        )
        full_path = os.path.join(stash_directory, dst_filename)
        with open(full_path, 'w') as f:
            json.dump(flat_ast, f, indent=2)
    else:
        print(json.dumps(flat_ast, indent=2))
        

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="League daily parser for Strat-O-Matic Report files")
    parser.add_argument('--stash', nargs='?', dest='dir',
                        help='directory to dump ASTs to')
    parser.add_argument('--league', choices=['blb', 'hof'], default='blb',
                        help='league the data belongs to')
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    args = parser.parse_args()
    
    main(args.file, args.dir, args.league)
