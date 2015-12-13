from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from blb.models.core import Base
from blb.models.mlb import Team

Session = sessionmaker()

def main(data_file):
    engine = create_engine('sqlite:///blb.db')
    Session.configure(bind=engine)
    session = Session()
    
    Base.metadata.create_all(engine)

    count = 0
    with open(data_file, 'r') as f:
        lines = f.readlines()
        keys = [key.strip().lower() for key in lines[0].split(',')]
        for line in lines[1:]:
            values = [value.strip() for value in line.split(',')]
            kwargs = dict(zip(keys, values))
            team = Team(**kwargs)
            session.add(team)
            count += 1
    session.commit()

    print "Inserted {} items".format(count)
            

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Import MLB team data from a file into the db')
    parser.add_argument('file', metavar='FILE', help='the MLB teams file to parse')
    args = parser.parse_args()

    main(args.file)
    
    
    
