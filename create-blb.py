import json

from blb.models.blb import (
    BLBDivision,
    BLBLeague,
    BLBSeason,
    BLBTeam
)

from data.sql_store import SQLStore


def main(db_file, data_file):
    store = SQLStore(db_file)

    with open(data_file) as fp:
        blb_dict = json.load(fp)

    league = store.get_or_create_blb_league(blb_dict).result()

    for season_dict in blb_dict['seasons']:
        season = store.get_or_create_blb_season({
            'year': season_dict['year'],
            'name': season_dict['name'],
            'league_id': league.id
            }).result()
        for division_dict in season_dict['divisions']:
            division = store.get_or_create_blb_division({
                'name': division_dict['name'],
                'season_id': season.id
                }).result()
            for team_dict in division_dict['teams']:
                team = store.get_or_create_blb_team({
                    'location': team_dict['location'],
                    'nickname': team_dict['nickname'],
                    'abbreviation': team_dict['abbreviation'],
                    'division_id': division.id,
                    'season_id': season.id
                    }).result()

                
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Create BLB leagues from JSON file")
    parser.add_argument('db', metavar='DB', help='the DB file')
    parser.add_argument('file', metavar="FILE", help="the input file")
    args = parser.parse_args()
    
    main(args.db, args.file)
