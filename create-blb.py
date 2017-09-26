import json

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

from data.exceptions import (
    InvalidLeagueException,
    InvalidPlayerException,
    InvalidYearException
)


def get_or_create_league(data):
    league_name = data['name']
    league = session.query(BLBLeague).filter(BLBLeague.name == league_name).one_or_none()
    if league is None:
        print "Creating League: {}".format(league_name)
        league = BLBLeague.from_dict(data)
        session.add(league)
        session.commit()
    return league


def get_or_create_season(data, league_id):
    fg_season = session.query(FGSeason).filter(
        FGSeason.year == data['year']
    ).one_or_none()
        
    season_name = data['name']
    season = session.query(BLBSeason).filter(and_(
        BLBSeason.league_id == league_id,
        BLBSeason.name == season_name)
    ).one_or_none()
    if season is None:
        print "Creating Season: {}".format(season_name)
        season = BLBSeason.from_dict({
            'name': season_name,
            'league_id': league_id,
            'fg_season_id': fg_season.id
            })
        session.add(season)
        session.commit()
    return season


def get_or_create_division(data, season_id):
    division_name = data['name']
    division = session.query(BLBDivision).filter(and_(
        BLBDivision.name == division_name,
        BLBDivision.season_id == season_id)
        ).one_or_none()
    if division is None:
        print "Creating Division: {}".format(division_name)
        division = BLBDivision.from_dict({
            'name': division_name,
            'season_id': season_id
            })
        session.add(division)
        session.commit()
    return division


def get_or_create_team(data, season_id, division_id):
    team = session.query(BLBTeam).filter(and_(
        BLBTeam.location == data['location'],
        BLBTeam.nickname == data['nickname'],
        BLBTeam.abbreviation == data['abbreviation'],
        BLBTeam.season_id == season_id
        )).one_or_none()
    if team is None:
        print "Creating Team: {} {}".format(data['location'], data['nickname'])
        team = BLBTeam.from_dict({
            'location': data['location'],
            'nickname': data['nickname'],
            'abbreviation': data['abbreviation'],
            'division_id': division_id,
            'season_id': season_id
            })
        session.add(team)
        session.commit()
    return team


def main(db_file, data_file):
    global session
    
    ENGINE = create_engine('sqlite:///{}'.format(db_file))
    Session = sessionmaker(bind=ENGINE)
    session = Session()

    with open(data_file) as fp:
        blb_dict = json.load(fp)

    league = get_or_create_league(blb_dict)

    for season_dict in blb_dict['seasons']:
        season = get_or_create_season(season_dict, league.id)
        for division_dict in season_dict['divisions']:
            division = get_or_create_division(division_dict, season.id)
            for team_dict in division_dict['teams']:
                team = get_or_create_team(team_dict, season.id, division.id)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Create BLB leagues from JSON file")
    parser.add_argument('db', metavar='DB', help='the DB file')
    parser.add_argument('file', metavar="FILE", help="the input file")
    args = parser.parse_args()
    
    main(args.db, args.file)
