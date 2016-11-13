#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from blb.models.core import Base
from blb.models.fangraphs import FGSeason, FGPlayer, \
    FGPlayerSeason, FGBatting, FGPitching, FGTeam

from blb.models.util import FG_BATTING_TO_DB,\
    FG_PITCHING_TO_DB, clean_value, clean_key


def main(file_type, year, db_file, data_file):
    ENGINE = create_engine('sqlite:///{}'.format(db_file))
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    
    Base.metadata.create_all(ENGINE)

    season = session.query(FGSeason).filter(FGSeason.year == year).one_or_none()
    if season is None:
        season = FGSeason(year=year)
        session.add(season)

    if file_type == 'batting':
        key_map = FG_BATTING_TO_DB
        StatsClass = FGBatting
    else:
        key_map = FG_PITCHING_TO_DB
        StatsClass = FGPitching

    count = 0
    with open(data_file, 'r') as f:
        lines = f.readlines()
        keys = [key_map[clean_key(key)] for key in lines[0].split(',')[2:-1]]
        for line in lines[1:]:
            values = [clean_value(value) for value in line.split(',')]

            # Determine if the player exists
            player_id = values[-1].strip()
            player = session.query(FGPlayer).filter(FGPlayer.id == player_id).one_or_none()
            if player is None:
                first_name, last_name = [clean_value(name) for name in values[0].split(' ', 1)]
                player = FGPlayer(id=player_id, last_name=last_name, first_name=first_name)
                session.add(player)

            # Determine if player exists for this season
            player_season = session.query(FGPlayerSeason).\
                            filter(and_(FGPlayerSeason.player_id == player.id,
                                        FGPlayerSeason.season_id == season.id)).one_or_none()
            if player_season is None:
                player_season = FGPlayerSeason(player_id=player.id, season_id=season.id)
                team = session.query(FGTeam).filter(FGTeam.nickname == values[1]).first()
                if team is not None:
                    if player_season.teams is None:
                        player_seasons = [team]
                    else:
                        player_season.teams.append(team)
                session.add(player_season)
            
            player_values = values[2:-1]
            kwargs = dict(zip(keys, player_values))
            stats = StatsClass(**kwargs)
            stats.player_season = player_season
            session.add(stats)
            count += 1
    session.commit()

    print "Inserted {} items".format(count)

if __name__ == '__main__':
    import argparse
    from os.path import basename

    parser = argparse.ArgumentParser(description='Import Fangraphs player data from a file into the db')
    parser.add_argument('db', metavar='DB', help='the DB file')
    parser.add_argument('file', metavar='FILE', help='the Fangraphs file to parse')
    args = parser.parse_args()

    base = basename(args.file)
    base, _ = base.split('.')
    source, stat, year = base.split('-')

    main(stat, year, args.db, args.file)
    
    
    
