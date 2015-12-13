from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from blb.models.core import Base
from blb.models.fangraphs import Season, Player, \
    PlayerSeason, Batting, Team

Session = sessionmaker()

# Map Fangraphs column names to our column names
FG_BATTING_TO_DB = {
    'G': 'g',
    'PA': 'pa',
    'HR': 'hr',
    'R': 'r',
    'RBI': 'rbi',
    'SB': 'sb',
    'BB%': 'bb_pct',
    'K%': 'k_pct',
    'ISO': 'iso',
    'BABIP': 'babip',
    'AVG': 'avg',
    'OBP': 'obp',
    'SLG': 'slg',
    'wOBA': 'woba',
    'wRC+': 'wrc_plus',
    'BsR': 'bsr',
    'Off': 'off',
    'Def': 'defense',
    'WAR': 'war',
    'AB': 'ab',
    'H': 'h',
    '1B': 'single',
    '2B': 'double',
    '3B': 'triple',
    'BB': 'bb',
    'IBB': 'ibb',
    'SO': 'so',
    'HBP': 'hbp',
    'GDP': 'gdp',
    'CS': 'cs',
    'GB': 'gb',
    'FB': 'fb',
    'LD': 'ld',
    'IFFB': 'iffb'
}

def main(data_file, year):
    engine = create_engine('sqlite:///blb.db')
    Session.configure(bind=engine)
    session = Session()
    
    Base.metadata.create_all(engine)

    season = session.query(Season).filter(Season.year == year).first()
    if season is None:
        season = Season(year=year)
        session.add(season)

    count = 0
    with open(data_file, 'r') as f:
        lines = f.readlines()
        keys = [FG_BATTING_TO_DB[key.strip().strip('"')] for key in lines[0].split(',')[2:-1]]
        for line in lines[1:]:
            values = [value.strip().strip('"').strip('%').strip() for value in line.split(',')]

            # Determine if the player exists
            player_id = values[-1].strip()
            player = session.query(Player).filter(Player.id == player_id).first()
            if player is None:
                first_name, last_name = [name.strip() for name in values[0].split(' ', 1)]
                player = Player(id=player_id, last_name=last_name, first_name=first_name)
                session.add(player)

            # Determine if player exists for this season
            player_season = session.query(PlayerSeason).\
                            filter(and_(PlayerSeason.player_id == player.id,
                                        PlayerSeason.season_id == season.id)).first()
            if player_season is None:
                player_season = PlayerSeason(player_id=player.id, season_id=season.id)
                session.add(player_season)
            
            # team = session.query(Team).filter(Team.nickname == values[1]).first()
            
            batting_values = values[2:-1]
            kwargs = dict(zip(keys, batting_values))
            kwargs['player_season_id'] = player_season.id
            batting = Batting(**kwargs)
            session.add(batting)
            count += 1
    session.commit()

    print "Inserted {} items".format(count)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Import Fangraphs player data from a file into the db')
    parser.add_argument('year', metavar='YEAR', help='the Fangraphs year')
    parser.add_argument('file', metavar='FILE', help='the Fangraphs file to parse')
    args = parser.parse_args()

    main(args.file, args.year)
    
    
    
