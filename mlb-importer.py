#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from blb.models.core import Base
from blb.models.fangraphs import FGTeam

def main(db_file, data_file):
    ENGINE = create_engine('sqlite:///{}'.format(db_file))
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    
    Base.metadata.create_all(ENGINE)

    count = 0
    with open(data_file, 'r') as f:
        lines = f.readlines()
        keys = [key.strip().lower() for key in lines[0].split(',')]
        for line in lines[1:]:
            values = [value.strip() for value in line.split(',')]
            kwargs = dict(zip(keys, values))
            team = FGTeam(**kwargs)
            session.add(team)
            count += 1
    session.commit()

    print "Inserted {} items".format(count)
            

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Import MLB team data from a file into the db')
    parser.add_argument('db', metavar='DB', help='the DB file')
    parser.add_argument('file', metavar='FILE', help='the MLB teams file to parse')
    args = parser.parse_args()

    main(args.db, args.file)
    
    
    
